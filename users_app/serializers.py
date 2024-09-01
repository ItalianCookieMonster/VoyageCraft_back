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


from rest_framework import serializers
from .models import Preference


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
            'climate',
            'landscape',
            'tourism_type',
            'trip_duration',
            'cost_level',
            'accessibility',
            'family_friendly'
        ]
        if value not in allowed_types:
            raise serializers.ValidationError("Invalid preference type.")
        return value

    def validate(self, data):
        preference_type = data.get('preference_type')
        preference_value = data.get('preference_value')

        valid_values = {
            'climate': ['Sunny', 'Cloudy', 'Rainy', 'Cold', 'Warm', 'Tropical', 'Snowy'],
            'landscape': ['Beach', 'Mountains', 'Forest', 'Desert', 'Urban/Cities', 'Countryside', 'Lakes/Rivers'],
            'tourism_type': ['Cultural', 'Adventure', 'Relaxation', 'Nature', 'Nightlife', 'Family-friendly',
                             'Shopping'],
            'trip_duration': ['1-3 days', '4-7 days', '1-2 weeks', '2 weeks or more'],
            'cost_level': ['Low', 'Medium', 'High'],
            'accessibility': ['True', 'False'],
            'family_friendly': ['True', 'False']
        }

        if preference_type in valid_values and preference_value not in valid_values[preference_type]:
            raise serializers.ValidationError(f"Invalid preference value for {preference_type}.")

        return data
