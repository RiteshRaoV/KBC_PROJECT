from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserPreference

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
        
        return redirect('start_quiz')  
    
    return render(request, 'quizTemplates/preferences.html')
