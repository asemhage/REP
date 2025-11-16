from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from listings.models import Property


class PropertyEndpointsTests(APITestCase):
    def setUp(self):
        self.investor = get_user_model().objects.create_user(
            username="investor",
            email="investor@example.com",
            password="StrongPass123",
            role="investor",
        )
        self.tenant = get_user_model().objects.create_user(
            username="tenant",
            email="tenant@example.com",
            password="StrongPass123",
            role="tenant",
        )

    def authenticate(self, username: str, password: str) -> str:
        url = reverse("auth-login")
        response = self.client.post(url, {"username": username, "password": password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["token"]

    def test_investor_can_create_property(self):
        token = self.authenticate("investor", "StrongPass123")
        url = reverse("property-list")
        payload = {
            "title": "شقة حديثة",
            "description": "شقة مريحة في وسط المدينة",
            "address": "123 Main St",
            "city": "Tripoli",
            "property_type": "apartment",
            "status": "available",
            "daily_rate": "150.00",
        }
        response = self.client.post(url, payload, format="json", HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Property.objects.filter(title="شقة حديثة").exists())

    def test_tenant_cannot_create_property(self):
        token = self.authenticate("tenant", "StrongPass123")
        url = reverse("property-list")
        payload = {
            "title": "شقة tenant",
            "address": "456 Street",
            "city": "Benghazi",
            "property_type": "apartment",
            "status": "available",
            "daily_rate": "120.00",
        }
        response = self.client.post(url, payload, format="json", HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_can_list_available_properties(self):
        Property.objects.create(
            owner=self.investor,
            title="فيلا فاخرة",
            description="",
            address="Coastal Road",
            city="Misrata",
            property_type="villa",
            status=Property.Status.AVAILABLE,
            daily_rate="500.00",
        )
        url = reverse("property-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
