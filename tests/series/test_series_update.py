from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.races.models import Series
from tests.config import (
    IMAGE_PATH,
    LARGE_PHOTO,
    TEST_LOGGER_NAME,
)
from tests.utils import (
    get_simple_upload_file,
    get_user,
)

logger = getLogger(TEST_LOGGER_NAME)


class TestSeriesUpdate(TestCase):
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
        self.valid_data = {
            "name": "Formula 1",
            "category": "car",
            "description": "The pinnacle of motorsport.",
        }

    def test_success_full_update(self) -> None:
        response = self.api_client.put(
            self.series_url,
            self.valid_data
            | {
                "name": "MotoGP",
                "category": "moto",
                "description": "Two-wheel racing.",
            },
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.series.refresh_from_db()
        self.assertEqual(self.series.name, "MotoGP")
        self.assertEqual(self.series.category, "moto")
        self.assertEqual(self.series.description, "Two-wheel racing.")

    def test_success_partial_update(self) -> None:
        partial_updates = [
            {"name": "MotoGP"},
            {"category": "moto"},
            {"description": "Two-wheel racing."},
        ]

        for data in partial_updates:
            response = self.api_client.patch(
                self.series_url,
                data,
                HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
            )
            logger.debug("%s %s: %s", self._testMethodName, data, response.text)
            self.assertEqual(response.status_code, 200)
            self.series.refresh_from_db()
            field, value = next(iter(data.items()))
            self.assertEqual(getattr(self.series, field), value)

    def test_update_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.put(
            self.series_url,
            self.valid_data,
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_update_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.put(
            self.series_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_full_update_without_required_fields(self) -> None:
        required_fields = ["name", "category"]
        for field in required_fields:
            data = {k: v for k, v in self.valid_data.items() if k != field}
            response = self.api_client.put(
                self.series_url,
                data,
                HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
            )
            logger.debug("%s [%s]: %s", self._testMethodName, field, response.text)
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.json())

    def test_update_with_empty_name(self) -> None:
        response = self.api_client.patch(
            self.series_url,
            {"name": "   "},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())

    def test_update_with_too_long_name(self) -> None:
        response = self.api_client.patch(
            self.series_url,
            {"name": "a" * 1000},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())

    def test_update_with_invalid_category(self) -> None:
        response = self.api_client.patch(
            self.series_url,
            {"category": "invalid"},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("category", response.json())

    def test_update_with_too_long_description(self) -> None:
        response = self.api_client.patch(
            self.series_url,
            {"description": "a" * 10_000},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("description", response.json())

    def test_update_nonexistent_series(self) -> None:
        response = self.api_client.patch(
            reverse("series-detail", kwargs={"slug": "nonexistent-series"}),
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)

    def test_update_logo(self) -> None:
        response = self.api_client.patch(
            self.series_url,
            {"logo": get_simple_upload_file(IMAGE_PATH)},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.series.refresh_from_db()
        self.assertIsNotNone(self.series.logo)

    def test_update_with_large_logo(self) -> None:
        response = self.api_client.patch(
            self.series_url,
            {"logo": get_simple_upload_file(LARGE_PHOTO)},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("logo", response.json())
