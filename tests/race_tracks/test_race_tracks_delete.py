from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.race_tracks.models import Track
from tests.config import IMAGE_PATH, TEST_LOGGER_NAME
from tests.utils import get_simple_upload_file, get_user

logger = getLogger(TEST_LOGGER_NAME)


class TestRaceTrackDelete(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.ordinary_user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)
        cls.ordinary_user_token = AccessToken.for_user(cls.ordinary_user)
        cls.staff_token = AccessToken.for_user(cls.staff)

    def setUp(self) -> None:
        self.track = Track.objects.create(
            name="Circuit de Monaco",
            country="MC",
            city="Monte Carlo",
            length_km="3.34",
        )
        self.track_url = reverse("track-detail", kwargs={"slug": self.track.slug})
        self.valid_data = {
            "name": "Circuit de Monaco Updated",
            "country": "MC",
            "city": "Monte Carlo",
            "length_km": "3.34",
            "lap_record": "00:01:10.166000",
            "number_of_turns": 19,
        }
        self.valid_data_with_map_image = self.valid_data.copy() | {
            "map_image": get_simple_upload_file(IMAGE_PATH)
        }

    def test_delete_success(self) -> None:
        response = self.api_client.delete(
            self.track_url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.status_code)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Track.objects.filter(pk=self.track.pk).exists())

    def test_delete_by_ordinary_user_forbidden(self) -> None:
        response = self.api_client.delete(
            self.track_url,
            HTTP_AUTHORIZATION=f"Bearer {self.ordinary_user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.status_code)
        self.assertEqual(response.status_code, 403)

    def test_delete_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.delete(self.track_url)
        logger.debug("%s: %s", self._testMethodName, response.status_code)
        self.assertEqual(response.status_code, 401)

    def test_delete_nonexistent_track(self) -> None:
        response = self.api_client.delete(
            reverse("track-detail", kwargs={"slug": "nonexistent-track"}),
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.status_code)
        self.assertEqual(response.status_code, 404)
