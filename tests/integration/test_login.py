from json import loads
from logging import getLogger

from django.test import TestCase
from django.urls import reverse

from apps.users.models import User
from tests.config import TEST_LOGGER_NAME

logger = getLogger(TEST_LOGGER_NAME)


class TestLogin(TestCase):
    login_url = reverse("login")

    def setUp(self) -> None:
        self.password = "MyPassword1234!"
        self.user = User.objects.create_user(
            email="smile@example.com",
            username="smile",
            password=self.password,
            first_name="smile",
            last_name="kun",
        )
        self.valid_data = {
            "email": "smile@example.com",
            "password": self.password,
        }

    def test_success_login(self) -> None:
        response = self.client.post(self.login_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        data = loads(response.text)
        self.assertIn("access", data)
        self.assertIn("refresh", data)

    def test_wrong_password(self) -> None:
        self.valid_data["password"] = "WrongPassword1!"
        response = self.client.post(self.login_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email or password.", loads(response.text)["non_field_errors"][0])

    def test_wrong_email(self) -> None:
        self.valid_data["email"] = "notexist@example.com"
        response = self.client.post(self.login_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email or password.", loads(response.text)["non_field_errors"][0])

    def test_invalid_email_format(self) -> None:
        self.valid_data["email"] = "notanemail"
        response = self.client.post(self.login_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertEqual("Enter a valid email address.", loads(response.text)["email"][0])

    def test_inactive_user(self) -> None:
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        response = self.client.post(self.login_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn("User account is disabled.", loads(response.text)["non_field_errors"][0])

    def test_missing_email(self) -> None:
        del self.valid_data["email"]
        response = self.client.post(self.login_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)

    def test_missing_password(self) -> None:
        del self.valid_data["password"]
        response = self.client.post(self.login_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)