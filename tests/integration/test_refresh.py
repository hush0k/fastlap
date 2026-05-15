from json import loads
from logging import getLogger

from django.test import TestCase
from django.urls import reverse

from apps.users.models import User
from tests.config import TEST_LOGGER_NAME
from unittest.mock import patch
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

logger = getLogger(TEST_LOGGER_NAME)


class TestRefresh(TestCase):
    login_url = reverse("login")
    refresh_url = reverse("token_refresh")

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="smile@example.com",
            username="smile",
            password="MyPassword1234!",
            first_name="smile",
            last_name="kun",
        )
        login_response = self.client.post(self.login_url, {
            "email": "smile@example.com",
            "password": "MyPassword1234!",
        })
        self.refresh_token = loads(login_response.text)["refresh"]

    def test_success_refresh(self) -> None:
        response = self.client.post(self.refresh_url, {"refresh": self.refresh_token})
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", loads(response.text))

    def test_invalid_token(self) -> None:
        response = self.client.post(self.refresh_url, {"refresh": "invalidtoken"})
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 401)

    def test_missing_token(self) -> None:
        response = self.client.post(self.refresh_url, {})
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)

    def test_token_already_used(self) -> None:
        self.client.post(self.refresh_url, {"refresh": self.refresh_token})
        response = self.client.post(self.refresh_url, {"refresh": self.refresh_token})
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 401)

    def test_expired_token(self) -> None:
        refresh = RefreshToken.for_user(self.user)
        refresh.set_exp(lifetime=timedelta(seconds=-1))

        response = self.client.post(self.refresh_url, {"refresh": str(refresh)})
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 401)





