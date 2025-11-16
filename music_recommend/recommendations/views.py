from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from django.utils import timezone

from .models import Recommendation, CachedResponse
from .serializers import RecommendationSerializer, CachedResponseSerializer
from users.models import UserProfile
from core.utils import refresh_spotify_token


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    @action(detail=True, methods=['get'], url_path='fetch')
    def fetch_recommendations(self, request, pk=None):

        # 1. Get user
        try:
            user = UserProfile.objects.get(id=pk)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # 2. Refresh access token
        access_token = refresh_spotify_token(user)
        if not access_token:
            return Response({"error": "Spotify not connected or token invalid"}, status=400)

        # 3. Determine genres
        genres_list = user.favorite_genres if user.favorite_genres else ["pop"]
        genres = ",".join(genres_list)

        # 4. Spotify API call
        url = "https://api.spotify.com/v1/recommendations"
        params = {
            "limit": 20,
            "seed_genres": genres
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(url, headers=headers, params=params)

        # 5. Handle invalid JSON response
        try:
            data = response.json()
        except Exception:
            return Response({
                "error": "Invalid response from Spotify",
                "details": response.text
            }, status=400)

        # 6. Validate Spotify API structure
        if "tracks" not in data:
            return Response({
                "error": "Spotify API did not return tracks",
                "details": data
            }, status=400)

        # 7. Save recommendation history
        Recommendation.objects.create(
            user=user,
            tracks=data["tracks"],
            fetched_at=timezone.now()
        )

        # 8. Cache API response
        CachedResponse.objects.update_or_create(
            user=user,
            defaults={
                "data": data,
                "updated_at": timezone.now()
            }
        )

        # 9. Final response
        return Response({
            "message": "Recommendations fetched successfully",
            "count": len(data["tracks"]),
            "tracks": data["tracks"]
        })


class CachedResponseViewSet(viewsets.ModelViewSet):
    queryset = CachedResponse.objects.all()
    serializer_class = CachedResponseSerializer
