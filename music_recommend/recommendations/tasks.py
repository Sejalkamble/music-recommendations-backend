
from celery import shared_task
from users.models import UserProfile
from .services import fetch_recommendations_internal


@shared_task
def refresh_recommendations_for_user(user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return {"error": "User not found"}

    return fetch_recommendations_internal(user)
