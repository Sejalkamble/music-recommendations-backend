from rest_framework import viewsets
from .models import UserEngagementSummary
from .serializers import UserEngagementSummarySerializer


class UserEngagementSummaryViewSet(viewsets.ModelViewSet):
    queryset = UserEngagementSummary.objects.all()
    serializer_class = UserEngagementSummarySerializer
