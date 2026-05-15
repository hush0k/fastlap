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


class TestDriverCreate(TestCase):
    drivers_url = reverse("drivers-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.ordinary_user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)

        cls.ordinary_user_token = AccessToken.for_user(cls.ordinary_user)
        cls.staff_token = AccessToken.for_user(cls.staff)

    def setUp(self) -> None:
        self.valid_data = {
            "first_name": "Luca",
            "last_name": "Verstani",
            "nationality": "NL",
            "date_of_birth": "1998-07-14",
            "number": 27,
            "bio": "Aggressive yet consistent F1 driver known for strong qualifying pace and late-braking overtakes. Started in karting at age 6 and progressed through Formula 2 before debuting in Formula 1.",
            "is_active": True,
        }
        self.valid_data_with_profile_image = self.valid_data.copy() | {
            "profile_image": get_simple_upload_file(IMAGE_PATH)
        }

    def test_success_create(self) -> None:
        response = self.api_client.post(
            self.drivers_url,
            self.valid_data_with_profile_image,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Driver.objects.filter(id=response.json()["id"]).exists())

        driver = Driver.objects.get(id=response.json()["id"])

        self.assertEqual(driver.first_name, self.valid_data["first_name"])
        self.assertEqual(driver.last_name, self.valid_data["last_name"])
        self.assertEqual(driver.number, self.valid_data["number"])
        self.assertEqual(str(driver.nationality), self.valid_data["nationality"])

    def test_create_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.post(
            self.drivers_url,
            self.valid_data,
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_create_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.post(
            self.drivers_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_create_with_large_profile_image(self) -> None:
        self.valid_data["profile_image"] = get_simple_upload_file(LARGE_PHOTO)
        response = self.api_client.post(
            self.drivers_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Max image size is", response.text)

    def test_create_with_nonexistent_nationality(self) -> None:
        self.valid_data["nationality"] = "XX"
        response = self.api_client.post(
            self.drivers_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)

    def test_create_without_required_fields(self) -> None:
        required_fields = ["first_name", "last_name", "nationality"]

        for field in required_fields:
            data = {k: v for k, v in self.valid_data.items() if k != field}
            response = self.api_client.post(
                self.drivers_url,
                data,
                HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
            )
            logger.debug("%s [%s]: %s", self._testMethodName, field, response.text)

            self.assertEqual(response.status_code, 400)
            self.assertIn("This field is required.", str(response.json()[field]))

    def test_create_with_first_name_too_long(self) -> None:
        self.valid_data["first_name"] = "a" * 101
        response = self.api_client.post(
            self.drivers_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", response.json())

    def test_create_with_last_name_too_long(self) -> None:
        self.valid_data["last_name"] = "a" * 101
        response = self.api_client.post(
            self.drivers_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("last_name", response.json())

    def test_create_with_bio_too_long(self) -> None:
        self.valid_data["bio"] = "a" * 15001
        response = self.api_client.post(
            self.drivers_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("bio", str(response.json()))
