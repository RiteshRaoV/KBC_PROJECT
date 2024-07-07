from django.contrib.auth.decorators import login_required
from .models import UserPreference
import requests
from .models import UserPreference, QuizAttempt,UserResponse
from django.utils import timezone
from django.http import JsonResponse
from django.utils.http import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from urllib.parse import urlencode
import time
import random
import html


@login_required
def set_preferences(request):
    if request.method == 'POST':
        UserPreference.objects.filter(user=request.user).delete()
        
        preferences = [
            {'topic': request.POST['topic_1'], 'difficulty': request.POST['difficulty_1']},
            {'topic': request.POST['topic_2'], 'difficulty': request.POST['difficulty_2']},
            {'topic': request.POST['topic_3'], 'difficulty': request.POST['difficulty_3']}
        ]
        
        for pref in preferences:
            UserPreference.objects.create(user=request.user, **pref)
        
        return redirect('take_quiz')  
    
    return render(request, 'quizTemplates/preferences.html')


# Base API URL
API_URL = "https://opentdb.com/api.php"

@login_required
def start_quiz(request):
    preferences = UserPreference.objects.filter(user=request.user)

    if not preferences.exists():
        return redirect('set-preferences')

    questions = []
    max_retries = 5  # Set a limit for retries to avoid infinite loops

    for pref in preferences:
        retries = 0
        params = {
            'amount': 5,
            'type': 'multiple'
        }
        if pref.topic.lower() != 'any':
            params['category'] = pref.topic
        if pref.difficulty.lower() != 'any':
            params['difficulty'] = pref.difficulty

        url = f"{API_URL}?{urlencode(params)}"
        
        while retries < max_retries:
            print(f"Fetching questions from: {url}")
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                response_code = data.get('response_code')
                if response_code == 0:
                    for items in data.get('results'):
                        question = {
                                'question': html.unescape(items['question']).replace('\"',"'"),
                                'options': items['incorrect_answers'],
                                'difficulty':items['difficulty'],
                                'answer': 1
                        }
                        index = random.randrange(0, 4)
                        question['options'].insert(index, items['correct_answer'])
                        question['answer'] = index
                        questions.append(question)
                    break
                else:
                    print(f"Response code {response_code} received. Retrying...")
            else:
                print(f"Failed to fetch questions for topic {pref.topic} and difficulty {pref.difficulty}. Status code: {response.status_code}")

            retries += 1
            time.sleep(2)  

    # Save quiz attempt
    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        topic=",".join([str(pref.topic) for pref in preferences if pref.topic.lower() != 'any']),
        difficulty=",".join([pref.difficulty for pref in preferences if pref.difficulty.lower() != 'any']),
        started_at=timezone.now()
    )
    
    return JsonResponse({'questions': questions, 'quiz_attempt_id': quiz_attempt.id})
    # return render(request, 'quizTemplates/take_quiz.html', {'questions': questions, 'quiz_attempt_id': quiz_attempt.id})


@login_required
def submit_quiz(request, quiz_attempt_id):
    quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id, user=request.user)

    if request.method == 'POST':
        for question in request.POST:
            if question.startswith('question_'):
                question_text = request.POST[question]
                selected_option = request.POST.get(question)
                correct_option = request.POST.get(f'correct_option_{question}')

                UserResponse.objects.create(
                    quiz_attempt=quiz_attempt,
                    question_text=question_text,
                    selected_option=selected_option,
                    correct_option=correct_option,
                )
                
        quiz_attempt.completed_at = timezone.now()
        quiz_attempt.save()

        return redirect('quiz_results', quiz_attempt_id=quiz_attempt.id)

    return render(request, 'quiz/quiz_results.html', {'quiz_attempt': quiz_attempt})