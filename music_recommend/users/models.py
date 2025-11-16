from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    spotify_access_token = models.TextField(null=True, blank=True)
    spotify_refresh_token = models.TextField(null=True, blank=True)
    spotify_token_expires = models.DateTimeField(null=True, blank=True)
    favorite_genres = models.JSONField(default=list)
    favorite_artists = models.JSONField(default=list)
    moods = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
