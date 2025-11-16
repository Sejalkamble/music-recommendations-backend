from django.db import models
from users.models import UserProfile

class UserEngagementSummary(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    total_plays = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    total_skips = models.IntegerField(default=0)

    def __str__(self):
        return f"Engagement summary for {self.user.email}"
