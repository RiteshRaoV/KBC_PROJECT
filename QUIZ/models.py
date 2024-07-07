from django.db import models
from django.conf import settings

class UserPreference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}: {self.topic} ({self.difficulty})"

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Quiz by {self.user.username} on {self.topic} ({self.difficulty}) at {self.started_at}"

class UserResponse(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=1000)
    selected_option = models.CharField(max_length=1000)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"Response for {self.quiz_attempt} - {self.question_text}"
