from logging import getLogger

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.races.models import Race, Series
from tests.config import TEST_LOGGER_NAME

logger = getLogger(TEST_LOGGER_NAME)


class TestRaceRetrieve(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()

        cls.series = Series.objects.create(name="Formula 1", category="car")
        cls.race = Race.objects.create(
            name="Monaco Grand Prix",
            series=cls.series,
            round_number=8,
            scheduled_at="2025-06-01T14:00:00Z",
            status="upcoming",
            watch_platform="f1_tv",
        )
        cls.race_url = reverse("races-detail", kwargs={"slug": cls.race.slug})

    def test_success_retrieve(self) -> None:
        response = self.api_client.get(self.race_url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["id"], self.race.id)
        self.assertEqual(data["name"], self.race.name)
        self.assertEqual(data["series"], self.race.series.id),
        self.assertEqual(data["round_number"], self.race.round_number)
        self.assertEqual(data["scheduled_at"], self.race.scheduled_at)
        self.assertEqual(data["status"], self.race.status)
        self.assertEqual(data["watch_platform"], self.race.watch_platform)

    def test_retrieve_nonexistent_race_404(self) -> None:
        response = self.api_client.get(
            reverse("races-detail", kwargs={"slug": "nonexistent-race"})
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)
