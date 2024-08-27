from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users_app.models import User


class UserRegistrationTestCase(APITestCase):

    def test_register_user(self):
        """
        Given an user with corrected credentials
        When registering a new user
        Then the user should be created
        And a 201 status code should be returned
        """
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username,
                         'testuser')

    def test_register_user_with_invalid_data(self):
        """
        Given an user with incorrect credentials
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
        self.assertEqual(User.objects.count(), 0)


class UserAuthTestCase(APITestCase):

    def setUp(self):
        """
        Set up method for user authentication tests.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

    def test_login_user(self):
        """
        Given an user with correct credentials
        When logging in
        Then a token pair should be returned
        And a 200 status code should be returned
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_with_invalid_credentials(self):
        """
        Given an user with incorrect credentials
        When logging in
        Then a token pair should not be returned
        And a 401 status code should be returned
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
