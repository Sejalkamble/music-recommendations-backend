
import requests
from django.utils import timezone
from django.core.cache import cache

from users.models import UserProfile
from core.utils import refresh_spotify_token
from .models import Recommendation, CachedResponse


def fetch_recommendations_internal(user: UserProfile):
    """
    Internal reusable function.
    Called by View + Celery async task.
    """

    # 1. Refresh Spotify token if expired
    access_token = refresh_spotify_token(user)
    if not access_token:
        return {"error": "Spotify not connected"}

    # 2. Build request to Spotify API
    genres = ",".join(user.favorite_genres or ["pop"])

    url = "https://api.spotify.com/v1/recommendations"
    params = {"limit": 20, "seed_genres": genres}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers, params=params)

    try:
        data = response.json()
    except Exception:
        data = None

    if not data or "tracks" not in data:
        return {
            "error": "Invalid response from Spotify",
            "details": response.text,
        }

    # 3. Save Recommendation log
    Recommendation.objects.create(
        user=user,
        tracks=data["tracks"],
        fetched_at=timezone.now(),
    )

    # 4. Save/update cache table (DB)
    CachedResponse.objects.update_or_create(
        user=user,
        defaults={"data": data, "updated_at": timezone.now()},
    )

    # 5. Save Redis cache (faster repeat)
    cache_key = f"rec_user_{user.id}"
    cache.set(cache_key, data, timeout=3600)  # 1 hour

    return {"success": True, "data": data}
