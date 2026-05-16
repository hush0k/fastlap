from logging import getLogger

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.common.enums import RaceStatusEnum, WatchPlatformEnum
from apps.races.models import Race, Series
from tests.config import TEST_LOGGER_NAME

logger = getLogger(TEST_LOGGER_NAME)


class TestRaceList(TestCase):
    races_url = reverse("races-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()

        cls.series_f1 = Series.objects.create(name="Formula 1", category="car")
        cls.series_motogp = Series.objects.create(name="MotoGP", category="moto")

        cls.race_monaco = Race.objects.create(
            name="Monaco Grand Prix",
            series=cls.series_f1,
            round_number=8,
            scheduled_at="2025-06-01T14:00:00Z",
            status=RaceStatusEnum.UPCOMING,
            watch_platform=WatchPlatformEnum.F1_TV,
        )
        cls.race_bahrain = Race.objects.create(
            name="Bahrain Grand Prix",
            series=cls.series_f1,
            round_number=1,
            scheduled_at="2025-03-02T15:00:00Z",
            status=RaceStatusEnum.FINISHED,
            watch_platform=WatchPlatformEnum.DAZN,
        )
        cls.race_motogp_qatar = Race.objects.create(
            name="Qatar MotoGP",
            series=cls.series_motogp,
            round_number=1,
            scheduled_at="2025-03-30T19:00:00Z",
            status=RaceStatusEnum.FINISHED,
            watch_platform=WatchPlatformEnum.YOUTUBE,
        )

    def test_success_list(self) -> None:
        response = self.api_client.get(self.races_url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 3)

    def test_filter_by_series(self) -> None:
        response = self.api_client.get(self.races_url, {"series": self.series_f1.id})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)

    def test_filter_by_status(self) -> None:
        response = self.api_client.get(self.races_url, {"status": "finished"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)

    def test_filter_by_watch_platform(self) -> None:
        response = self.api_client.get(self.races_url, {"watch_platform": "youtube"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["id"], self.race_motogp_qatar.id)

    def test_search_by_name(self) -> None:
        response = self.api_client.get(self.races_url, {"search": "Monaco"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["id"], self.race_monaco.id)

    def test_ordering_by_scheduled_at(self) -> None:
        response = self.api_client.get(self.races_url, {"ordering": "scheduled_at"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        dates = [item["scheduled_at"] for item in response.json()["results"]]
        self.assertEqual(dates, sorted(dates))

    def test_ordering_by_round_number(self) -> None:
        response = self.api_client.get(
            self.races_url,
            {"ordering": "round_number", "series": self.series_f1.id},
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        rounds = [item["round_number"] for item in response.json()["results"]]
        self.assertEqual(rounds, sorted(rounds))
