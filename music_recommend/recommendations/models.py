from django.db import models
from users.models import UserProfile

class Recommendation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tracks = models.JSONField()  # List of recommended tracks
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendations for {self.user.email} at {self.fetched_at}"


class CachedResponse(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    data = models.JSONField()  # Raw Spotify API response
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cached response for {self.user.email}"
