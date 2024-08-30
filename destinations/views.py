from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Destination
from users_app.models import Preference
from .serializers import DestinationSerializer


# views.py

class DestinationRecommendationView(APIView):

    def get(self, request):
        user = request.user

        # Recupera le preferenze dell'utente
        preferences = Preference.objects.filter(user=user)

        if not preferences.exists():
            return Response({"message": "No preferences found for user."}, status=status.HTTP_400_BAD_REQUEST)

        # Costruisci il filtro di query basato sulle preferenze
        query = Q()

        print(f"Preferences for user {user.username}:")
        for preference in preferences:
            print(f"Preference type: {preference.preference_type}, value: {preference.preference_value}")
            if preference.preference_type == 'landscape':
                query &= Q(landscape=preference.preference_value)
            elif preference.preference_type == 'tourism_type':
                query &= Q(tourism_type=preference.preference_value)
            elif preference.preference_type == 'cost_level':
                query &= Q(cost_level=preference.preference_value)
            elif preference.preference_type == 'family_friendly':
                query &= Q(family_friendly=preference.preference_value.lower() == 'true')
            elif preference.preference_type == 'accessibility':
                query &= Q(accessibility=preference.preference_value.lower() == 'true')

        # Applica il filtro alla query
        filtered_destinations = Destination.objects.filter(query).distinct()

        print(f"Query results: {filtered_destinations}")

        # Serializza i risultati
        serializer = DestinationSerializer(filtered_destinations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)