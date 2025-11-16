# import requests
# from django.conf import settings
# from django.utils import timezone
# from users.models import UserProfile

# def refresh_spotify_token(user: UserProfile):
#     """
#     Refresh the Spotify access token safely.
#     Handles cases where token_expiry is None or expired.
#     """

#     # 1. If expiry missing or token expired → refresh it
#     if user.spotify_token_expires:
#         if user.spotify_token_expires > timezone.now():
#             # Token is still valid
#             return user.spotify_access_token

#     # 2. If no refresh token exists → user never connected to Spotify
#     if not user.spotify_refresh_token:
#         return None

#     # 3. Call Spotify to refresh token
#     url = "https://accounts.spotify.com/api/token"
#     payload = {
#         "grant_type": "refresh_token",
#         "refresh_token": user.spotify_refresh_token,
#         "client_id": settings.SPOTIFY_CLIENT_ID,
#         "client_secret": settings.SPOTIFY_CLIENT_SECRET,
#     }

#     response = requests.post(url, data=payload)

#     # 4. Handle invalid/empty response
#     try:
#         token_data = response.json()
#     except:
#         return None

#     access_token = token_data.get("access_token")
#     if not access_token:
#         return None

#     # 5. Calculate new token expiry
#     expires_in = token_data.get("expires_in", 3600)

#     # 6. Save user tokens
#     user.spotify_access_token = access_token
#     user.spotify_token_expires = timezone.now() + timezone.timedelta(seconds=expires_in)
#     user.save()

#     return access_token
import requests
from django.conf import settings
from django.utils import timezone

def refresh_spotify_token(user):
    # Valid token check
    if user.spotify_token_expires and user.spotify_token_expires > timezone.now():
        return user.spotify_access_token

    if not user.spotify_refresh_token:
        return None

    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": user.spotify_refresh_token,
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    }

    r = requests.post(token_url, data=data)
    if r.status_code != 200:
        return None

    try:
        token_data = r.json()
    except Exception:
        return None

    access_token = token_data.get("access_token")
    expires_in = token_data.get("expires_in", 3600)

    if not access_token:
        return None

    user.spotify_access_token = access_token
    user.spotify_token_expires = timezone.now() + timezone.timedelta(seconds=expires_in)
    user.save()
    return access_token
