from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import Coalesce
from django.db.models import Q, When, Case, Sum, IntegerField, Value
from .models import Destination
from .utils import get_user_preferences, build_strict_query, build_type_query, build_flexible_query
from .serializers import DestinationSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


# views.py

class DestinationRecommendationView(generics.GenericAPIView):
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        user = request.user
        user_preferences = get_user_preferences(user)

        if not user_preferences.exists():
            return Response({"message": "User has no preferences set."}, status=status.HTTP_400_BAD_REQUEST)

            # Build queries
        strict_query = build_strict_query(user_preferences)
        type_query = build_type_query(user_preferences)
        flexible_query = build_flexible_query(user_preferences)

        try:
            recommended_destinations = Destination.objects.filter(strict_query)
            recommended_destinations = recommended_destinations.filter(type_query)
            recommended_destinations = recommended_destinations.filter(flexible_query)
            recommended_destinations = recommended_destinations.distinct()

        except Exception as e:
            print(f"Error occurred during filtering: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not recommended_destinations.exists():
            return self.handle_no_recommendations()

        ordered_destinations = self.annotate_and_order_destinations(recommended_destinations, user_preferences)
        destination_serializer = DestinationSerializer(ordered_destinations, many=True)
        return Response(destination_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def handle_no_recommendations() -> Response:
        generic_recommendations = Destination.objects.filter(
            Q(family_friendly=True) | Q(accessibility=True)
        ).distinct()
        print("Didn't find recommedetions so I am here ")
        if not generic_recommendations.exists():
            return Response({
                "message": "No destinations match your preferences. No alternative destinations available at this time."
            }, status=status.HTTP_404_NOT_FOUND)

        limited_recommendations = generic_recommendations.order_by('name')[:10]
        destination_serializer = DestinationSerializer(limited_recommendations, many=True)
        return Response({
            "message": "No exact matches found based on your preferences. Here are some alternative destinations.",
            "recommendations": destination_serializer.data
        }, status=status.HTTP_200_OK)

    def annotate_and_order_destinations(self, destinations, user_preferences) -> Destination:
        preference_mapping = {
            'accessibility': 'accessibility',
            'family_friendly': 'family_friendly',
            'climate': 'weather_data__weather',
            'landscape': 'landscape',
            'tourism_type': 'tourism_type',
            'cost_level': 'cost_level',
            'travel_duration': 'type',
        }

        relevance_annotation = Sum(
            Case(
                *[
                    When(
                        Q(**{preference_mapping[pref.preference_type]: pref.preference_value}),
                        then=1
                    )
                    for pref in user_preferences if pref.preference_type in preference_mapping
                ],
                default=Value(0),
                output_field=IntegerField()
            )
        )
        destinations = destinations.annotate(relevance=Coalesce(relevance_annotation, 0))
        return destinations.order_by('relevance')
