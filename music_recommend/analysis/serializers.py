from rest_framework import serializers
from .models import UserEngagementSummary


class UserEngagementSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEngagementSummary
        fields = '__all__'
