from rest_framework import serializers
from .models import Itinerary, ItineraryStep

class ItineraryStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryStep
        fields = ['id', 'description', 'date', 'order']

class ItinerarySerializer(serializers.ModelSerializer):
    steps = ItineraryStepSerializer(many=True, required=False)

    class Meta:
        model = Itinerary
        fields = ['id', 'user', 'name', 'description', 'start_date', 'end_date', 'destination', 'steps']

    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        itinerary = Itinerary.objects.create(**validated_data)
        for step_data in steps_data:
            ItineraryStep.objects.create(itinerary=itinerary, **step_data)
        return itinerary

    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.save()

        existing_steps = {step.id: step for step in instance.steps.all()}
        for step_data in steps_data:
            step_id = step_data.get('id')
            if step_id:
                step = existing_steps.pop(step_id)
                step.description = step_data.get('description', step.description)
                step.date = step_data.get('date', step.date)
                step.order = step_data.get('order', step.order)
                step.save()
            else:
                ItineraryStep.objects.create(itinerary=instance, **step_data)
        for step in existing_steps.values():
            step.delete()

        return instance

