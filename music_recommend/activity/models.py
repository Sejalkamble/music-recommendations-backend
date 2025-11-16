from django.db import models
from users.models import UserProfile

class UserActivity(models.Model):
    ACTION_CHOICES = (
        ('play', 'Play'),
        ('like', 'Like'),
        ('skip', 'Skip'),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    track_id = models.CharField(max_length=200)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.track_id} - {self.action}"

