from logging import getLogger

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.races.models import Series
from tests.config import TEST_LOGGER_NAME

logger = getLogger(TEST_LOGGER_NAME)


class TestSeriesList(TestCase):
    series_url = reverse("series-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()

        cls.series_f1 = Series.objects.create(name="Formula 1", category="car")
        cls.series_motogp = Series.objects.create(name="MotoGP", category="moto")
        cls.series_le_mans = Series.objects.create(name="Le Mans", category="endurance")

    def test_success_list(self) -> None:
        response = self.api_client.get(self.series_url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 3)

    def test_filter_by_category(self) -> None:
        response = self.api_client.get(self.series_url, {"category": "car"})
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["id"], self.series_f1.id)

    def test_search_by_name(self) -> None:
        response = self.api_client.get(self.series_url, {"search": "MotoGP"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["id"], self.series_motogp.id)

    def test_search_by_description(self) -> None:
        self.series_f1.description = "The pinnacle of motorsport."
        self.series_f1.save()

        response = self.api_client.get(self.series_url, {"search": "pinnacle"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["id"], self.series_f1.id)

    def test_ordering_by_name(self) -> None:
        response = self.api_client.get(self.series_url, {"ordering": "name"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        names = [item["name"] for item in response.json()["results"]]
        self.assertEqual(names, sorted(names))

    def test_ordering_by_name_desc(self) -> None:
        response = self.api_client.get(self.series_url, {"ordering": "-name"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        names = [item["name"] for item in response.json()["results"]]
        self.assertEqual(names, sorted(names, reverse=True))
