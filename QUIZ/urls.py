from django.urls import path
from . import views

urlpatterns = [
    path('set-preferences/',views.set_preferences,name='set_preferences'),
    path('take_quiz/', views.start_quiz, name='take_quiz'),
    path('submit_quiz/<int:quiz_attempt_id>/', views.submit_quiz, name='submit_quiz'),
]
