from .models import Destination
from rest_framework import serializers


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'name', 'description', 'type', 'landscape', 'tourism_type', 'cost_level', 'family_friendly',
                  'accessibility']


