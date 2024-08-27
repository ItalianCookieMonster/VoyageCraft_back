from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users_app.models import User, Preference


class BaseTestCase(APITestCase):
    """
    Base class for tests with common setup and utility methods.
    """

    def setUp(self):
        """
        Common setup for all tests.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.preference_data = {
            'preference_type': 'Music',
            'preference_value': 'Jazz'
        }
        self.client.force_authenticate(user=self.user)  # Authenticate by default
        self.create_preference_url = reverse('preferences')

    def authenticate_user(self):
        """
        Authenticate the test client with the created user.
        """
        self.client.force_authenticate(user=self.user)

    def obtain_token(self):
        """
        Obtain a token for the user.
        """
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'password123'}
        return self.client.post(url, data, format='json')


class UserRegistrationTestCase(BaseTestCase):

    def test_register_user(self):
        """
        Given a user with correct credentials
        When registering a new user
        Then the user should be created
        And a 201 status code should be returned
        """
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Ensure there are now two users
        self.assertEqual(User.objects.get(username='newuser').username, 'newuser')

    def test_register_user_with_invalid_data(self):
        """
        Given a user with incorrect credentials
        When registering a new user
        Then the user should not be created
        And a 400 status code should be returned
        """
        url = reverse('register')
        data = {
            'username': '',
            'email': 'invalid-email',
            'password': 'pwd',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class UserAuthTestCase(BaseTestCase):

    def test_login_user(self):
        """
        Given a user with correct credentials
        When logging in
        Then a token pair should be returned
        And a 200 status code should be returned
        """
        response = self.obtain_token()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_with_invalid_credentials(self):
        """
        Given a user with incorrect credentials
        When logging in
        Then a token pair should not be returned
        And a 401 status code should be returned
        """
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PreferenceTestCase(BaseTestCase):

    def test_create_preference(self):
        """
        Given an authenticated user
        When creating a new preference
        Then the preference should be created
        And a 201 status code should be returned
        """
        response = self.client.post(self.create_preference_url, self.preference_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Preference.objects.count(), 1)
        self.assertEqual(Preference.objects.get().preference_type, 'Music')

    def test_create_preference_with_invalid_data(self):
        """
        Given an authenticated user
        And invalid data
        When creating a new preference
        Then a 400 status code should be returned
        """
        invalid_data = {'preference_type': '', 'preference_value': ''}
        response = self.client.post(self.create_preference_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('preference_type', response.data)
        self.assertIn('preference_value', response.data)

    def test_update_preference(self):
        """
        Given an authenticated user
        And an ID of a preference
        When updating a preference
        Then the preference should be updated
        And a 200 status code should be returned
        """
        preference = Preference.objects.create(user=self.user, **self.preference_data)
        url = reverse('update_preference', kwargs={'pk': preference.id})
        updated_data = {'preference_type': 'Music', 'preference_value': 'Rock'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Preference.objects.get().preference_value, 'Rock')

    def test_update_nonexistent_preference(self):
        """
        Given an authenticated user
        And an ID of a preference that does not exist
        When updating a preference
        Then a 404 status code should be returned
        """
        url = reverse('update_preference', kwargs={'pk': 999})  # Non-existent ID
        updated_data = {'preference_type': 'Music', 'preference_value': 'Rock'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_preference(self):
        """
        Given an authenticated user
        And an ID of a preference
        When deleting a preference
        Then the preference should be deleted
        """
        preference = Preference.objects.create(user=self.user, **self.preference_data)
        url = reverse('delete_preference', kwargs={'pk': preference.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Preference.objects.count(), 0)

    def test_delete_nonexistent_preference(self):
        """
        Given an authenticated user
        And an ID of a preference that does not exist
        When deleting a preference
        Then a 404 status code should be returned
        """
        url = reverse('delete_preference', kwargs={'pk': 999})  # Non-existent ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_preference_unauthenticated(self):
        """
        Given an unauthenticated user
        When creating a new preference
        Then a 401 status code should be returned
        """
        self.client.force_authenticate(user=None)
        response = self.client.post(self.create_preference_url, self.preference_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)