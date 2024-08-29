from .models import User, Preference
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'age', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True, 'required': False, },
            'username': {'required': False},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ['id', 'user', 'preference_type', 'preference_value']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }

    @staticmethod
    def validate_preference_type(value):
        allowed_types = [
            "Preferred Climate",
            "Preferred Landscape/Scenery",
            "Type of Tourism",
            "Travel Duration",
            "Travel Companions",
            "Budget Preferences",
            "Accessibility Needs"
        ]
        if value not in allowed_types:
            raise serializers.ValidationError("Invalid preference type.")
        return value

