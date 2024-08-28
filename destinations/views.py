from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Destination, WeatherData, Activity
from .serializers import DestinationSerializer
from users_app.serializers import PreferenceSerializer
from users_app.models import Preference
from django.db.models import Q


class DestinationRecommendationView(generics.GenericAPIView):
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user = self.request.user
        user_preferences = Preference.objects.filter(user=user)

        query = Q()

        travel_duration = None
        travel_with_family = False

        for pref in user_preferences:
            if pref.preference_type == 'Preferred Climate':
                query &= Q(weather_data__weather=pref.preference_value)
            elif pref.preference_type == 'Preferred Landscape/Scenery':
                query &= Q(landscape=pref.preference_value)
            elif pref.preference_type == 'Type of Tourism':
                query &= Q(tourism_type=pref.preference_value)
            elif pref.preference_type == 'Budget Preferences':
                query &= Q(cost_level=pref.preference_value)
            elif pref.preference_type == 'Accessibility Needs':
                if pref.preference_value.lower() == 'yes':
                    query &= Q(accessibility=True)

        if travel_duration:
            if travel_duration in ['1-3 days', '4-7 days']:
                query &= Q(type__in=['City', 'POI'])
            elif travel_duration in ['1-2 weeks', '2 weeks or more']:
                query &= Q(type__in=['City', 'Region'])

        if travel_with_family:
            query &= Q(family_friendly=True)

        recommended_destinations = Destination.objects.filter(query).distinct()
        destination_serializer = DestinationSerializer(recommended_destinations, many=True)

        return Response(destination_serializer.data, status=status.HTTP_200_OK)
