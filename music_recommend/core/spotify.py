import os
import base64
import requests
from django.conf import settings

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


class SpotifyAuth:
    def get_auth_url(self):
        scopes = "user-read-email user-read-private"

        return (
            f"{SPOTIFY_AUTH_URL}"
            f"?client_id={settings.SPOTIFY_CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={settings.SPOTIFY_REDIRECT_URI}"
            f"&scope={scopes}"
        )

    def get_token(self, code):
        auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        }

        response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)

        return response.json()
