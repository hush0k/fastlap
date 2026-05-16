from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.drivers.models import Driver
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


class TestDriverUpdate(TestCase):
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
        self.valid_data = {
            "first_name": "Max",
            "last_name": "Verstani",
            "nationality": "NL",
        }

    def test_success_full_update(self) -> None:
        response = self.api_client.put(
            self.driver_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.first_name, "Max")

    def test_success_partial_update(self) -> None:
        response = self.api_client.patch(
            self.driver_url,
            {"first_name": "Max"},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.first_name, "Max")

    def test_update_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.put(
            self.driver_url,
            self.valid_data,
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_update_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.put(
            self.driver_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_full_update_without_required_fields(self) -> None:
        required_fields = ["first_name", "last_name", "nationality"]
        for field in required_fields:
            data = {k: v for k, v in self.valid_data.items() if k != field}
            response = self.api_client.put(
                self.driver_url,
                data,
                HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
            )
            logger.debug("%s [%s]: %s", self._testMethodName, field, response.text)
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.json())

    def test_update_with_first_name_too_long(self) -> None:
        self.valid_data["first_name"] = "a" * 101
        response = self.api_client.patch(
            self.driver_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", response.json())

    def test_update_with_last_name_too_long(self) -> None:
        self.valid_data["last_name"] = "a" * 101
        response = self.api_client.patch(
            self.driver_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("last_name", response.json())

    def test_update_with_bio_too_long(self) -> None:
        self.valid_data["bio"] = "a" * 15001
        response = self.api_client.patch(
            self.driver_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("bio", response.json())

    def test_update_nonexistent_driver(self) -> None:
        response = self.api_client.patch(
            reverse("drivers-detail", kwargs={"slug": "nonexistent-driver"}),
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)

    def test_update_profile_image(self) -> None:
        response = self.api_client.patch(
            self.driver_url,
            {"profile_image": get_simple_upload_file(IMAGE_PATH)},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.driver.refresh_from_db()
        self.assertIsNotNone(self.driver.profile_image)

    def test_update_with_large_profile_image(self) -> None:
        response = self.api_client.patch(
            self.driver_url,
            {"profile_image": get_simple_upload_file(LARGE_PHOTO)},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("profile_image", response.json())
