from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.drivers.models import Driver
from tests.config import (
    TEST_LOGGER_NAME,
)
from tests.utils import (
    get_user,
)

logger = getLogger(TEST_LOGGER_NAME)


class TestDriverDelete(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.ordinary_user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)

        cls.ordinary_user_token = AccessToken.for_user(cls.ordinary_user)
        cls.staff_token = AccessToken.for_user(cls.staff)

    def setUp(self) -> None:
        self.driver = Driver.objects.create(
            first_name="Luca",
            last_name="Verstani",
            nationality="NL",
        )
        self.driver_url = reverse("drivers-detail", kwargs={"slug": self.driver.slug})

    def test_success_delete(self) -> None:
        response = self.api_client.delete(
            self.driver_url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Driver.objects.filter(id=self.driver.id).exists())

    def test_delete_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.delete(self.driver_url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_delete_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.delete(
            self.driver_url,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_delete_not_existent_driver_404(self) -> None:
        Driver.objects.filter(id=self.driver.id).delete()
        response = self.api_client.delete(
            self.driver_url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)
