# import requests
# from django.shortcuts import redirect
# from django.conf import settings
# import urllib.parse

# def spotify_login(request):
#     scope = "user-read-private user-read-email"

#     query_params = {
#         "client_id": settings.SPOTIFY_CLIENT_ID,
#         "response_type": "code",
#         "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
#         "scope": scope,
#     }

#     url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(query_params)
#     return redirect(url)


# import base64
# import time
# from django.http import JsonResponse
# from django.conf import settings
# from users.models import UserProfile
# from django.utils import timezone

# def spotify_callback(request):
#     code = request.GET.get("code")

#     if not code:
#         return JsonResponse({"error": "Code not provided"}, status=400)

#     # Prepare token request
#     token_url = "https://accounts.spotify.com/api/token"
#     payload = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
#         "client_id": settings.SPOTIFY_CLIENT_ID,
#         "client_secret": settings.SPOTIFY_CLIENT_SECRET,
#     }

#     # Request Spotify token
#     response = requests.post(token_url, data=payload)
#     token_data = response.json()

#     if "access_token" not in token_data:
#         return JsonResponse({"error": "Failed to get token", "details": token_data}, status=400)

#     access_token = token_data["access_token"]
#     refresh_token = token_data.get("refresh_token")
#     expires_in = token_data["expires_in"]

#     # Fetch Spotify user profile
#     headers = {"Authorization": f"Bearer {access_token}"}
#     user_data = requests.get("https://api.spotify.com/v1/me", headers=headers).json()

#     email = user_data.get("email")

#     # Save or update user
#     user, created = UserProfile.objects.get_or_create(email=email)
#     user.spotify_access_token = access_token
#     user.spotify_refresh_token = refresh_token
#     user.spotify_token_expires = timezone.now() + timezone.timedelta(seconds=expires_in)
#     user.save()

#     return JsonResponse({
#         "message": "Spotify authentication successful",
#         "user": user.email,
#         "access_token": access_token,
#     })
import base64, requests, urllib
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from users.models import UserProfile

def spotify_login(request):
    scopes = "user-read-email user-read-private user-top-read"
    params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": scopes,
        "show_dialog": "true"
    }
    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    return redirect(url)

def spotify_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error":"no code"}, status=400)

    token_url = "https://accounts.spotify.com/api/token"
    auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    b64 = base64.b64encode(auth_str.encode()).decode()

    data = {
        "grant_type":"authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI
    }
    headers = {"Authorization": f"Basic {b64}"}

    r = requests.post(token_url, data=data, headers=headers)
    if r.status_code != 200:
        return JsonResponse({"error":"token exchange failed","details": r.text}, status=400)

    token_data = r.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in", 3600)

    # Get user's email from Spotify
    me = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {access_token}"})
    if me.status_code != 200:
        return JsonResponse({"error":"failed to fetch spotify user","details": me.text}, status=400)
    me_json = me.json()
    email = me_json.get("email")
    name = me_json.get("display_name") or email.split("@")[0]

    user, created = UserProfile.objects.get_or_create(email=email, defaults={"name": name})
    user.spotify_access_token = access_token
    user.spotify_refresh_token = refresh_token
    user.spotify_token_expires = timezone.now() + timezone.timedelta(seconds=expires_in)
    user.save()

    return JsonResponse({"message":"spotify connected", "email": email})
