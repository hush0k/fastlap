from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.common.enums import RaceStatusEnum, SeriesCategoryEnum, WatchPlatformEnum
from apps.races.models import Race, Series
from tests.config import TEST_LOGGER_NAME
from tests.utils import get_user

logger = getLogger(TEST_LOGGER_NAME)


class TestRaceDelete(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)
        cls.user_token = AccessToken.for_user(cls.user)
        cls.staff_token = AccessToken.for_user(cls.staff)

        cls.series = Series.objects.create(
            name="Formula 1", category=SeriesCategoryEnum.CAR
        )

    def setUp(self) -> None:
        self.race = Race.objects.create(
            name="Monaco Grand Prix",
            series=self.series,
            round_number=8,
            scheduled_at="2025-06-01T14:00:00Z",
            status=RaceStatusEnum.UPCOMING,
            watch_platform=WatchPlatformEnum.F1_TV,
        )
        self.race_url = reverse("races-detail", kwargs={"slug": self.race.slug})

    def test_success_delete(self) -> None:
        response = self.api_client.delete(
            self.race_url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Race.objects.filter(id=self.race.id).exists())

    def test_delete_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.delete(self.race_url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_delete_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.delete(
            self.race_url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_delete_nonexistent_race_404(self) -> None:
        Race.objects.filter(id=self.race.id).delete()
        response = self.api_client.delete(
            self.race_url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)
