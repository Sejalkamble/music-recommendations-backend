from rest_framework.routers import DefaultRouter
from django.urls import path, include

from users.views import UserProfileViewSet
from activity.views import UserActivityViewSet
from analysis.views import UserEngagementSummaryViewSet
from recommendations.views import RecommendationViewSet, CachedResponseViewSet
from core.views import spotify_login,spotify_callback
router = DefaultRouter()

router.register('users', UserProfileViewSet, basename='users')
router.register('activity', UserActivityViewSet, basename='activity')
router.register('analysis', UserEngagementSummaryViewSet, basename='analysis')
router.register('recommendations', RecommendationViewSet, basename='recommendations')
router.register('cache', CachedResponseViewSet, basename='cache')

urlpatterns = [
    path('', include(router.urls)),
    path("spotify/login/", spotify_login, name="spotify-login"),
    path("spotify/callback/", spotify_callback, name="spotify-callback"),
]

