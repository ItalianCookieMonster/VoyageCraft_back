from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'age']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }
