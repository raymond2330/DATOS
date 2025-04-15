from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "testuser@example.com",
            "password": "securepassword",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_create_user(self):
        response = self.client.post("/api/user/create/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_token_obtain(self):
        User.objects.create_user(username="testuser", email="testuser@example.com", password="securepassword")
        response = self.client.post("/api/token/", {"username": "testuser", "password": "securepassword"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
