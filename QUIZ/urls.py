from django.urls import path
from . import views

urlpatterns = [
    path('set-preferences/',views.set_preferences,name='set_preferences'),
    path('start-quiz/',views.set_preferences,name='start_quiz')
]
