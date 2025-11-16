from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthEndpointsTests(APITestCase):
    def test_register_creates_user_and_token(self):
        url = reverse("auth-register")
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
            "role": "tenant",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(username="testuser").exists())

    def test_login_returns_token_and_user(self):
        user = get_user_model().objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="StrongPass123",
        )

        url = reverse("auth-login")
        payload = {"username": user.username, "password": "StrongPass123"}

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], user.username)
