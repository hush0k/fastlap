from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.races.models import Series
from tests.config import (
    TEST_LOGGER_NAME,
)
from tests.utils import (
    get_user,
)

logger = getLogger(TEST_LOGGER_NAME)


class TestSeriesDelete(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.ordinary_user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)

        cls.ordinary_user_token = AccessToken.for_user(cls.ordinary_user)
        cls.staff_token = AccessToken.for_user(cls.staff)

    def setUp(self) -> None:
        self.series = Series.objects.create(
            name="Formula 1",
            category="car",
        )
        self.series_url = reverse("series-detail", kwargs={"slug": self.series.slug})

    def test_success_delete(self) -> None:
        response = self.api_client.delete(
            self.series_url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Series.objects.filter(id=self.series.id).exists())

    def test_delete_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.delete(self.series_url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_delete_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.delete(
            self.series_url,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_delete_nonexistent_series_404(self) -> None:
        Series.objects.filter(id=self.series.id).delete()
        response = self.api_client.delete(
            self.series_url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)
