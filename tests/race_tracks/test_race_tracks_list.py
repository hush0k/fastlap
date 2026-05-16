from logging import getLogger

from django.test import TestCase
from django.urls import reverse

from apps.race_tracks.models import Track
from tests.config import TEST_LOGGER_NAME

logger = getLogger(TEST_LOGGER_NAME)


class TestRaceTrackList(TestCase):
    tracks_url = reverse("track-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.track_monaco = Track.objects.create(
            name="Circuit de Monaco",
            country="MC",
            city="Monte Carlo",
            length_km="3.34",
        )
        cls.track_silverstone = Track.objects.create(
            name="Silverstone Circuit",
            country="GB",
            city="Silverstone",
            length_km="5.89",
        )
        cls.track_monza = Track.objects.create(
            name="Autodromo Nazionale Monza",
            country="IT",
            city="Monza",
            length_km="5.79",
        )
        cls.track_spa = Track.objects.create(
            name="Circuit de Spa-Francorchamps",
            country="BE",
            city="Stavelot",
            length_km="7.00",
        )

    def test_list_returns_all_tracks(self) -> None:
        response = self.client.get(self.tracks_url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 4)

    def test_filter_by_country(self) -> None:
        response = self.client.get(self.tracks_url + "?country=IT")
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["country_name"], "Italy")

    def test_filter_by_nonexistent_country(self) -> None:
        response = self.client.get(self.tracks_url + "?country=JP")
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 0)

    def test_search_by_name(self) -> None:
        response = self.client.get(self.tracks_url + "?search=Silverstone")
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["name"], "Silverstone Circuit")

    def test_search_by_city(self) -> None:
        response = self.client.get(self.tracks_url + "?search=Monza")
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["city"], "Monza")

    def test_search_no_results(self) -> None:
        response = self.client.get(self.tracks_url + "?search=Nonexistent")
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 0)

    def test_ordering_by_name_asc(self) -> None:
        response = self.client.get(self.tracks_url + "?ordering=name")
        logger.debug("%s: %s", self._testMethodName, response.text)
        names = [t["name"] for t in response.json()["results"]]
        self.assertEqual(names, sorted(names))

    def test_ordering_by_name_desc(self) -> None:
        response = self.client.get(self.tracks_url + "?ordering=-name")
        logger.debug("%s: %s", self._testMethodName, response.text)
        names = [t["name"] for t in response.json()["results"]]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_ordering_by_length_km_asc(self) -> None:
        response = self.client.get(self.tracks_url + "?ordering=length_km")
        logger.debug("%s: %s", self._testMethodName, response.text)
        lengths = [float(t["length_km"]) for t in response.json()["results"]]
        self.assertEqual(lengths, sorted(lengths))

    def test_ordering_by_length_km_desc(self) -> None:
        response = self.client.get(self.tracks_url + "?ordering=-length_km")
        logger.debug("%s: %s", self._testMethodName, response.text)
        lengths = [float(t["length_km"]) for t in response.json()["results"]]
        self.assertEqual(lengths, sorted(lengths, reverse=True))

    def test_response_fields(self) -> None:
        response = self.client.get(self.tracks_url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        track = response.json()["results"][0]
        expected_fields = {
            "id",
            "name",
            "slug",
            "country_name",
            "city",
            "length_km",
            "number_of_turns",
        }
        self.assertEqual(set(track.keys()), expected_fields)
