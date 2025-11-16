from rest_framework import serializers
from .models import Recommendation, CachedResponse


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'


class CachedResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CachedResponse
        fields = '__all__'
