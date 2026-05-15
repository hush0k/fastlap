from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.race_tracks.models import Track
from tests.config import IMAGE_PATH, LARGE_PHOTO, TEST_LOGGER_NAME
from tests.utils import get_simple_upload_file, get_user

logger = getLogger(TEST_LOGGER_NAME)


class TestRaceTrackCreate(TestCase):
    tracks_url = reverse("track-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.ordinary_user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)
        cls.ordinary_user_token = AccessToken.for_user(cls.ordinary_user)
        cls.staff_token = AccessToken.for_user(cls.staff)

    def setUp(self) -> None:
        self.valid_data = {
            "name": "Circuit de Monaco",
            "country": "MC",
            "city": "Monte Carlo",
            "length_km": "3.34",
            "lap_record": "00:01:10.166000",
            "number_of_turns": 19,
        }
        self.valid_data_with_map_image = self.valid_data.copy() | {
            "map_image": get_simple_upload_file(IMAGE_PATH)
        }

    def test_success_create(self) -> None:
        response = self.api_client.post(
            self.tracks_url,
            self.valid_data_with_map_image,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Track.objects.filter(name=self.valid_data["name"]).exists())

    def test_create_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.post(self.tracks_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_create_without_required_fields(self) -> None:
        required_fields = ["name", "country", "city", "length_km"]
        for field in required_fields:
            data = {k: v for k, v in self.valid_data.items() if k != field}
            response = self.api_client.post(
                self.tracks_url,
                data,
                HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
            )
            logger.debug("%s [%s]: %s", self._testMethodName, field, response.text)
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.json())

    def test_create_with_length_km_zero_or_negative(self) -> None:
        for i in [0, -1]:
            self.valid_data["length_km"] = i
            response = self.api_client.post(
                self.tracks_url,
                self.valid_data,
                HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
            )
            logger.debug("%s: %s", self._testMethodName, response.text)
            self.assertEqual(response.status_code, 400)
            self.assertIn("length_km", response.json())

    def test_create_with_invalid_country(self) -> None:
        self.valid_data["country"] = "XX"
        response = self.api_client.post(
            self.tracks_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("country", response.json())

    def test_create_with_large_map_image(self) -> None:
        self.valid_data["map_image"] = get_simple_upload_file(LARGE_PHOTO)
        response = self.api_client.post(
            self.tracks_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("map_image", response.json())

    def test_create_with_name_too_long(self) -> None:
        self.valid_data["name"] = "a" * 256
        self.valid_data["map_image"] = get_simple_upload_file(IMAGE_PATH)
        response = self.api_client.post(
            self.tracks_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())

    def test_create_with_city_too_long(self) -> None:
        self.valid_data["city"] = "a" * 101
        self.valid_data["map_image"] = get_simple_upload_file(IMAGE_PATH)
        response = self.api_client.post(
            self.tracks_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("city", response.json())

    def test_create_with_length_km_too_many_digits(self) -> None:
        self.valid_data["length_km"] = "12345678901.00"
        self.valid_data["map_image"] = get_simple_upload_file(IMAGE_PATH)
        response = self.api_client.post(
            self.tracks_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("length_km", response.json())

    def test_create_with_invalid_lap_record_format(self) -> None:
        self.valid_data["lap_record"] = "invalid"
        self.valid_data["map_image"] = get_simple_upload_file(IMAGE_PATH)
        response = self.api_client.post(
            self.tracks_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("lap_record", response.json())

    def test_create_with_negative_number_of_turns(self) -> None:
        self.valid_data["number_of_turns"] = -1
        self.valid_data["map_image"] = get_simple_upload_file(IMAGE_PATH)
        response = self.api_client.post(
            self.tracks_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("number_of_turns", response.json())

    def test_create_with_empty_map_image(self) -> None:
        self.valid_data["map_image"] = get_simple_upload_file(IMAGE_PATH, empty=True)
        response = self.api_client.post(
            self.tracks_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 400)
        self.assertIn("map_image", response.json())
