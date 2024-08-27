# chatbot/serializers.py

from rest_framework import serializers

class ChatbotSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    response = serializers.CharField(max_length=1000)
