from django.test import TestCase
from django.contrib.auth import get_user_model
# To generate our API url
from django.urls import reverse

# Test Client to make request to our api and check the response
from rest_framework.test import APIClient
# Contains the Status codes we can see,
# Just to make the test easy to understand
from rest_framework import status


# Constant to store the url will gonna be testing
# Create the create user url
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Named Public for noauthenticated users and private for autenticated
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        # Just have 1 client for our tests to reuse
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'mark@londonappdev.com',
            'password': 'mark123',
            'name': 'Mark'
        }
        # Make a request
        res = self.client.post(CREATE_USER_URL, payload)
        # Assert the return is 201 (Created)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Check is the user was created
        user = get_user_model().objects.get(**res.data)
        # Check if the passwrod is correct
        self.assertTrue(user.check_password(payload['password']))
        # Assert password is not returned
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': 'mark@londonappdev.com',
            'password': 'mark123',
            'name': 'Mark',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'mark@londonappdev.com',
            'password': 'ma',
            'name': 'Mark',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'mark@londonappdev.com',
            'password': 'mark123',
            'name': 'Mark'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(
            email='mark@londonappdev.com',
            password='mark123',
            name='Mark'
        )
        payload = {'email': 'mark@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            'email': 'mark@londonappdev.com',
            'password': 'mark123',
            'name': 'Mark'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': '@', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='silvia.christina@hotmail.com',
            password='testpass',
            name='Silvia'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'Silvia Christina', 'password': 'newpassword'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
