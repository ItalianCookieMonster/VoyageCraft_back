from .models import Itinerary, ItineraryStep
from rest_framework import serializers


class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'created_at', 'updated_at', 'destination']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        itinerary = Itinerary.objects.create(**validated_data)
        return itinerary


class ItineraryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'destination']
        extra_kwargs = {
            'id': {'read_only': True},
            'destination': {'required': False},
        }

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)





class ItineraryStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryStep
        fields = ['id', 'itinerary', 'step_order', 'stay_duration_hours', 'description', 'activity', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        itinerary_step = ItineraryStep.objects.create(**validated_data)
        return itinerary_step

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)