from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Case, When, IntegerField, Sum
from .models import Destination
from .permissions import IsAdminOrReadOnly
from .serializers import DestinationSerializer
from users_app.models import Preference


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAdminOrReadOnly]


class DestinationRecommendationView(generics.GenericAPIView):
    """
    View to provide destination recommendations based on user preferences.
    """

    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handles GET requests to provide destination recommendations.

        Retrieves user preferences, builds strict, type, and flexible queries,
        fetches matching destinations, calculates relevance, and returns the results.
        """
        user = request.user
        user_preferences = self.get_user_preferences(user)

        if not user_preferences.exists():
            return Response({"message": "User has no preferences set."}, status=status.HTTP_400_BAD_REQUEST)

        strict_query = self.build_strict_query(user_preferences)
        type_query = self.build_type_query(user_preferences)
        flexible_query = self.build_flexible_query(user_preferences)

        recommended_destinations = Destination.objects.filter(
            strict_query & type_query & flexible_query
        ).distinct()

        if not recommended_destinations.exists():
            return self.handle_no_recommendations()

        ordered_destinations = self.annotate_and_order_destinations(recommended_destinations, user_preferences)

        destination_serializer = DestinationSerializer(ordered_destinations, many=True)
        return Response(destination_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_user_preferences(user) -> Preference:
        """
        Retrieve all preferences for a given user.

        Args:
            user (User): The user for whom preferences are being retrieved.

        Returns:
            QuerySet: A queryset containing all preferences of the user.
        """
        return Preference.objects.filter(user=user)

    @staticmethod
    def build_strict_query(user_preferences) -> Q:
        """
        Build a strict query for filtering destinations based on user preferences.

        Args:
            user_preferences (QuerySet): A queryset of user preferences.

        Returns:
            Q: A Django Q object representing the strict query.
        """
        strict_query = Q()

        requires_accessibility = user_preferences.filter(preference_type='Accessibility').exists()
        requires_family_friendly = user_preferences.filter(preference_type='Family-friendly').exists()

        if requires_accessibility:
            strict_query &= Q(accessibility=True)
        if requires_family_friendly:
            strict_query &= Q(family_friendly=True)

        return strict_query

    def build_type_query(self, user_preferences) -> Q:
        """
        Build a query based on the type of destinations considering user preferences.

        Args:
            user_preferences (QuerySet): A queryset of user preferences.

        Returns:
            Q: A Django Q object representing the type query.
        """
        type_query = Q()
        has_duration_pref = False

        for pref in user_preferences:
            if pref.preference_type == 'Travel Duration':
                has_duration_pref = True
                type_query |= self.build_duration_query(pref.preference_value)

        return type_query | self.add_default_type_query(has_duration_pref)

    def build_flexible_query(self, user_preferences) -> Q:
        """
        Build a flexible query based on user preferences.

        Args:
            user_preferences (QuerySet): A queryset of user preferences.

        Returns:
            Q: A Django Q object representing the flexible query.
        """
        flexible_query = Q()
        has_climate_pref, has_landscape_pref, has_tourism_pref, has_budget_pref = False, False, False, False

        for pref in user_preferences:
            if pref.preference_type == 'Preferred Climate':
                flexible_query |= Q(weather_data__weather=pref.preference_value)
                has_climate_pref = True
            elif pref.preference_type == 'Preferred Landscape/Scenery':
                flexible_query |= Q(landscape=pref.preference_value)
                has_landscape_pref = True
            elif pref.preference_type == 'Type of Tourism':
                flexible_query |= Q(tourism_type=pref.preference_value)
                has_tourism_pref = True
            elif pref.preference_type == 'Budget Preferences':
                flexible_query |= Q(cost_level=pref.preference_value)
                has_budget_pref = True

        return flexible_query | self.add_default_flexible_queries(
            has_climate_pref, has_landscape_pref, has_tourism_pref, has_budget_pref
        )

    @staticmethod
    def build_duration_query(duration_pref: str) -> Q:
        """
        Build a query based on travel duration preference.

        Args:
            duration_pref (str): The user's travel duration preference.

        Returns:
            Q: A Django Q object representing the duration query.
        """
        if duration_pref in ['1-3 days', '4-7 days']:
            return Q(type__in=['City', 'POI'])
        elif duration_pref in ['1-2 weeks', '2 weeks or more']:
            return Q(type__in=['City', 'Region'])
        return Q()

    @staticmethod
    def add_default_flexible_queries(has_climate_pref: bool, has_landscape_pref: bool,
                                     has_tourism_pref: bool, has_budget_pref: bool) -> Q:
        """
        Add default flexible queries if no specific preferences are set.

        Args:
            has_climate_pref (bool): Whether a climate preference is set.
            has_landscape_pref (bool): Whether a landscape preference is set.
            has_tourism_pref (bool): Whether a tourism type preference is set.
            has_budget_pref (bool): Whether a budget preference is set.

        Returns:
            Q: A Django Q object representing the default flexible queries.
        """
        flexible_query = Q()
        if not has_climate_pref:
            flexible_query |= Q(weather_data__weather__in=['Sunny', 'Cloudy', 'Rainy', 'Hot', 'Cold'])
        if not has_landscape_pref:
            flexible_query |= Q(landscape__in=['Beach', 'Mountains', 'Urban', 'Countryside', 'Lakes/Rivers'])
        if not has_tourism_pref:
            flexible_query |= Q(
                tourism_type__in=['Cultural', 'Adventure', 'Relaxation', 'Nature', 'Nightlife', 'Family-friendly',
                                  'Shopping'])
        if not has_budget_pref:
            flexible_query |= Q(cost_level__in=['Low', 'Medium', 'High'])
        return flexible_query

    @staticmethod
    def add_default_type_query(has_duration_pref: bool) -> Q:
        """
        Add default query for destination type if no duration preference is set.

        Args:
            has_duration_pref (bool): Whether a duration preference is set.

        Returns:
            Q: A Django Q object representing the default type query.
        """
        if not has_duration_pref:
            return Q(type__in=['City', 'POI', 'Region'])
        return Q()

    @staticmethod
    def handle_no_recommendations() -> Response:
        """
        Handle the case where no exact recommendations are found.

        Returns:
            Response: A Response object with a message and general recommendations.
        """
        generic_recommendations = Destination.objects.filter(
            Q(family_friendly=True) | Q(accessibility=True)
        ).distinct()

        if not generic_recommendations.exists():
            return Response({
                "message": "No destinations match your preferences. No alternative destinations available at this time."
            }, status=status.HTTP_404_NOT_FOUND)

        # Return message and generic recommendations
        generic_recommendations = generic_recommendations.order_by('name')
        destination_serializer = DestinationSerializer(generic_recommendations, many=True)
        return Response({
            "message": "No exact matches found based on your preferences. Here are some alternative destinations.",
            "recommendations": destination_serializer.data
        }, status=status.HTTP_200_OK)

    @staticmethod
    def annotate_and_order_destinations(destinations, user_preferences) -> Destination:
        """
        Annotate and order destinations by relevance based on user preferences.

        Args:
            destinations (QuerySet): A queryset of destinations to annotate and order.
            user_preferences (QuerySet): A queryset of user preferences.

        Returns:
            QuerySet: A queryset of destinations ordered by relevance.
        """
        # Define preference categories and related fields to calculate relevance
        preference_mapping = {
            'Accessibility': 'accessibility',
            'Family-friendly': 'family_friendly',
            'Preferred Climate': 'weather_data__weather',
            'Preferred Landscape/Scenery': 'landscape',
            'Type of Tourism': 'tourism_type',
            'Budget Preferences': 'cost_level',
            'Travel Duration': 'type',
        }

        # Start building the annotation for relevance calculation
        relevance_annotation = Sum(
            Case(
                *[
                    When(
                        Q(**{preference_mapping[pref.preference_type]: pref.preference_value}),
                        then=1
                    )
                    for pref in user_preferences
                    if pref.preference_type in preference_mapping
                ],
                output_field=IntegerField()
            )
        )

        destinations = destinations.annotate(relevance=relevance_annotation)

        for destination in destinations:
            print(f"Destination: {destination.name}, Relevance: {destination.relevance}")

        # Order the destinations by the annotated relevance score in descending order
        ordered_destinations = destinations.order_by('-relevance')

        return ordered_destinations
