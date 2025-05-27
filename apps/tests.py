from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class RegisterUserAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('auth-register')
        self.user_data = {
            "email": "user@example.com",
            "password": "password",
            "full_name": "example_username",
            "phone_number": "+998901234567"
        }

    def test_register_user_successfully(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data["data"])
        self.assertEqual(response.data["data"]["user"]["email"], self.user_data["email"])
        self.assertEqual(response.data["data"]["user"]["full_name"], self.user_data["full_name"])
        self.assertEqual(response.data["data"]["user"]["phone_number"], self.user_data["phone_number"])


