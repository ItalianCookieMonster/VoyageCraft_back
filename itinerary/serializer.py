from rest_framework import serializers
from .models import Itinerary, ItineraryStep

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'description', 'start_date', 'end_date']
        extra_kwargs = {
            'id': {'read_only': True},
        }

class ItineraryStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryStep
        fields = ['id', 'itinerary', 'name', 'description', 'order', 'location', 'start_time', 'end_time']
        extra_kwargs = {
            'id': {'read_only': True},
            'itinerary': {'read_only': True},
        }
