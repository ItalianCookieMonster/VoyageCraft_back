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
        self.client.force_authenticate(user=self.user)
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
        data = {
            "preferences": [
                {
                    "preference_type": "Music",
                    "preference_value": "Jazz"
                }
            ]
        }

        response = self.client.post(self.create_preference_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Preference.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Preference.objects.get().preference_value, 'Jazz')

    def test_create_preference_with_invalid_data(self):
        """
        Given an authenticated user
        When creating a new preference with invalid data
        Then the preference should not be created
        And a 400 status code should be returned
        """
        invalid_data = {
            "preferences": [
                {
                    "preference_type": "",
                    "preference_value": ""
                }
            ]
        }

        response = self.client.post(self.create_preference_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Preference type not provided')

    def test_update_preference(self):
        """
        Given an authenticated user
        And the user has a preference
        When calling the PreferencesView
        Then the preference should be updated
        """

        preference = Preference.objects.create(user=self.user, **self.preference_data)
        updated_data = {
            "preferences": [
                {
                    "preference_type": "Music",
                    "preference_value": "Rock"
                }
            ]
        }

        response = self.client.post(self.create_preference_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Preference.objects.get(id=preference.id).preference_value, 'Rock')

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
        self.assertEqual(Preference.objects.filter(user=self.user).count(), 0)

    def test_delete_nonexistent_preference(self):
        """
        Given an authenticated user
        And an ID of a preference that does not exist
        When deleting a preference
        Then a 404 status code should be returned
        """
        url = reverse('delete_preference', kwargs={'pk': 999})  # ID non esistente

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_preference_unauthenticated(self):
        """
        Given an unauthenticated user
        When creating a new preference
        Then a 401 status code should be returned
        """
        self.client.force_authenticate(user=None)  # Logout
        response = self.client.post(self.create_preference_url, self.preference_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrieveUpdateUserViewTestCase(BaseTestCase):
    def setUp(self):
        """
        Set up specific to RetrieveUpdateUserViewTestCase.
        """
        super().setUp()
        self.url = reverse('update_user')

    def test_retrieve_user_details(self):
        """
        Given an authenticated user
        When requesting their details
        Then the correct user details should be returned
        And a 200 status code should be returned
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_update_user_details(self):
        """
        Given an authenticated user
        When updating their details with valid data
        Then the user details should be updated
        And a 200 status code should be returned
        """
        updated_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        response = self.client.patch(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')
        self.assertEqual(response.data['email'], 'updateduser@example.com')
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'User')

        # Ensure the changes are reflected in the database
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_update_user_with_invalid_data(self):
        """
        Given an authenticated user
        When updating their details with invalid data
        Then the user details should not be updated
        And a 400 status code should be returned
        """
        invalid_data = {
            'username': '',
            'email': 'not-an-email',
            'first_name': '',
            'last_name': ''
        }
        response = self.client.put(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
