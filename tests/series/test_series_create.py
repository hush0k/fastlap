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


class TestSeriesCreate(TestCase):
    series_url = reverse("series-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.ordinary_user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)

        cls.ordinary_user_token = AccessToken.for_user(cls.ordinary_user)
        cls.staff_token = AccessToken.for_user(cls.staff)

    def setUp(self) -> None:
        self.valid_data = {
            "name": "Formula 1",
            "category": "car",
            "description": "The pinnacle of motorsport.",
        }

    def test_success_create(self) -> None:
        response = self.api_client.post(
            self.series_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Series.objects.filter(name=self.valid_data["name"]).exists())

        series = Series.objects.get(name=self.valid_data["name"])

        self.assertEqual(series.name, self.valid_data["name"])
        self.assertEqual(series.category, self.valid_data["category"])
        self.assertEqual(series.description, self.valid_data["description"])

    def test_success_create_with_logo(self) -> None:
        data = self.valid_data.copy() | {"logo": get_simple_upload_file(IMAGE_PATH)}
        response = self.api_client.post(
            self.series_url,
            data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Series.objects.filter(name=self.valid_data["name"]).exists())

        series = Series.objects.get(name=self.valid_data["name"])
        self.assertIsNotNone(series.logo)

    def test_create_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.post(
            self.series_url,
            self.valid_data,
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_create_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.post(
            self.series_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_create_without_required_fields(self) -> None:
        required_fields = ["name", "category"]

        for field in required_fields:
            data = {k: v for k, v in self.valid_data.items() if k != field}
            response = self.api_client.post(
                self.series_url,
                data,
                HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
            )
            logger.debug("%s [%s]: %s", self._testMethodName, field, response.text)

            self.assertEqual(response.status_code, 400)
            self.assertIn("This field is required.", str(response.json()[field]))

    def test_create_with_empty_name(self) -> None:
        self.valid_data["name"] = "   "
        response = self.api_client.post(
            self.series_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())

    def test_create_with_invalid_category(self) -> None:
        self.valid_data["category"] = "invalid"
        response = self.api_client.post(
            self.series_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("category", response.json())

    def test_create_with_large_logo(self) -> None:
        self.valid_data["logo"] = get_simple_upload_file(LARGE_PHOTO)
        response = self.api_client.post(
            self.series_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("logo", response.json())

    def test_create_with_too_long_description(self) -> None:
        self.valid_data["description"] = "a" * 10_000
        response = self.api_client.post(
            self.series_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("description", response.json())
