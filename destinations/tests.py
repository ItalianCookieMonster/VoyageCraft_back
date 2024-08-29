from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Destination, WeatherData
from users_app.models import Preference

User = get_user_model()


class DestinationRecommendationViewTests(TestCase):
    def setUp(self):
        """
        Set up the test environment and create test data.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.destination1 = Destination.objects.create(
            name='Test Destination 1',
            type='City',
            landscape='Urban',
            tourism_type='Cultural',
            cost_level='Medium',
            family_friendly=True,
            accessibility=True
        )
        self.destination2 = Destination.objects.create(
            name='Test Destination 2',
            type='POI',
            landscape='Beach',
            tourism_type='Relaxation',
            cost_level='High',
            family_friendly=True,
            accessibility=False
        )

        WeatherData.objects.create(
            destination=self.destination1,
            month='January',
            weather='Sunny'
        )
        WeatherData.objects.create(
            destination=self.destination2,
            month='February',
            weather='Cloudy'
        )

        Preference.objects.create(user=self.user, preference_type='Preferred Climate', preference_value='Sunny')
        Preference.objects.create(user=self.user, preference_type='Preferred Landscape/Scenery',
                                  preference_value='Urban')
        Preference.objects.create(user=self.user, preference_type='Type of Tourism', preference_value='Cultural')
        Preference.objects.create(user=self.user, preference_type='Budget Preferences', preference_value='Medium')

    def test_recommendation_with_full_preferences(self):
        """
        Given: an authenticated user
        And: the user has all the preferences
        Then: when the user requests for the recommended destinations
        Then: the response should contain the recommended destinations

        """
        response = self.client.get('/api/v1/recommended-destinations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the recommended destinations match the expected output
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Destination 1')

    def test_recommendation_with_partial_preferences(self):
        """
        Given: an authenticated user
        And: the user has some of the preferences
        Then: when the user requests for the recommended destinations
        Then: the response should contain the recommended destinations
        """
        # Delete one preference to simulate partial preferences
        Preference.objects.filter(user=self.user, preference_type='Preferred Landscape/Scenery').delete()

        response = self.client.get('/api/v1/recommended-destinations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if at least one destination is returned based on remaining preferences
        self.assertGreaterEqual(len(response.data), 1)

    def test_recommendation_no_matching_destinations(self):
        """
        Given: an authenticated user
        And: the user has no matching destinations
        Then: when the user requests for the recommended destinations
        Then: the response should contain a message and generic recommendations
        """

        Preference.objects.filter(user=self.user).delete()
        Preference.objects.create(user=self.user, preference_type='Preferred Climate', preference_value='Snowy')
        Preference.objects.create(user=self.user, preference_type='Preferred Landscape/Scenery',
                                  preference_value='Desert')
        Preference.objects.create(user=self.user, preference_type='Type of Tourism', preference_value='Extreme Sports')
        Preference.objects.create(user=self.user, preference_type='Budget Preferences', preference_value='Luxury')

        response = self.client.get('/api/v1/recommended-destinations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'],
                         "No exact matches found based on your preferences. Here are some alternative destinations.")

        self.assertIn('recommendations', response.data)
        self.assertGreater(len(response.data['recommendations']), 0)

        for destination in response.data['recommendations']:
            self.assertIn('id', destination)
            self.assertIn('name', destination)
            self.assertIn('type', destination)

    def test_recommendation_with_no_preferences(self):
        """
        Given: an authenticated user
        And: the user has no preferences
        Then: when the user requests for the recommended destinations
        Then: the response should contain no destinations
        """
        # Remove all preferences for the user
        Preference.objects.filter(user=self.user).delete()

        response = self.client.get('/api/v1/recommended-destinations/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains the correct message
        self.assertEqual(response.data['message'], "User has no preferences set.")

    def test_relevance_annotation(self):
        ordered_destinations = self.annotate_and_order_destinations(
            Destination.objects.all(),
            Preference.objects.filter(user=self.user)
        )

        for d in ordered_destinations:
            print(f"Destination: {d.name}, Relevance: {d.relevance}")

    '''def test_recommendation_order_by_relevance(self):
        """
        Test that the recommendations are ordered by relevance.
        """
        Preference.objects.filter(user=self.user).delete()
        Preference.objects.create(user=self.user, preference_type='Preferred Climate', preference_value='Sunny')
        Preference.objects.create(user=self.user, preference_type='Preferred Landscape/Scenery',
                                  preference_value='Beach')
        Preference.objects.create(user=self.user, preference_type='Type of Tourism', preference_value='Relaxation')
        Preference.objects.create(user=self.user, preference_type='Budget Preferences', preference_value='High')

        Destination.objects.create(
            name='Test Destination 3',
            type='City',
            landscape='Beach',
            tourism_type='Relaxation',
            cost_level='High',
            family_friendly=True,
            accessibility=True
        )

        Destination.objects.create(
            name='Test Destination 4',
            type='City',
            landscape='Urban',
            tourism_type='Cultural',
            cost_level='Medium',
            family_friendly=True,
            accessibility=True
        )

        response = self.client.get('/api/v1/recommended-destinations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print("Destinations returned by relevance:")
        for destination in response.data:
            print(destination['name'], destination.get('relevance', 'No relevance'))

        # Continua con i test
        self.assertGreater(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Destination 1')
        self.assertEqual(response.data[1]['name'], 'Test Destination 2')'''


class DestinationRecommendationUnauthorizedTest(APITestCase):
    """
         Given: an unauthenticated user
         Then: when the user requests for the recommended destinations
         Then: the response should be 401 Unauthorized
    """

    def test_unauthorized_access(self):
        # Attempt to access the endpoint without authentication
        response = self.client.get('/api/v1/recommended-destinations/')

        # Check that the response is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
