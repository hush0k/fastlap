from logging import getLogger

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.teams.models import Team
from tests.config import TEST_LOGGER_NAME

logger = getLogger(TEST_LOGGER_NAME)


def create_team(**kwargs) -> Team:
    data = dict(
        name="Test Team",
        short_name="TST",
        country="US",
        founded_year=2000,
    )
    data.update(**kwargs)
    return Team.objects.create(**data)


class TestTeamList(TestCase):
    teams_url = reverse("teams-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.team_a = create_team(
            name="Alpha Team", short_name="ALT", country="US", founded_year=2000
        )
        cls.team_b = create_team(
            name="Beta Team", short_name="BET", country="GB", founded_year=2010
        )

    def test_list_returns_200(self) -> None:
        response = self.api_client.get(self.teams_url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)

    def test_list_fields_present(self) -> None:
        expected_fields = [
            "id",
            "name",
            "short_name",
            "logo",
            "banner",
            "slug",
            "country",
            "country_name",
        ]
        response = self.api_client.get(self.teams_url)

        logger.debug("%s: %s", self._testMethodName, response.text)

        result = response.json()["results"][0]
        for field in expected_fields:
            self.assertIn(field, result)

    def test_list_search_by_name(self) -> None:
        response = self.api_client.get(self.teams_url, {"search": "Alpha"})

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["name"], "Alpha Team")

    def test_list_search_by_short_name(self) -> None:
        response = self.api_client.get(self.teams_url, {"search": "BET"})

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_list_search_by_country(self) -> None:
        response = self.api_client.get(self.teams_url, {"search": "US"})

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_list_filter_by_country(self) -> None:
        response = self.api_client.get(self.teams_url, {"country": "GB"})

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["name"], "Beta Team")

    def test_list_filter_by_founded_year(self) -> None:
        response = self.api_client.get(self.teams_url, {"founded_year": 2000})
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["name"], "Alpha Team")

    def test_list_ordering_by_name_asc(self) -> None:
        response = self.api_client.get(self.teams_url, {"ordering": "name"})

        logger.debug("%s: %s", self._testMethodName, response.text)

        names = [t["name"] for t in response.json()["results"]]
        self.assertEqual(names, sorted(names))

    def test_list_ordering_by_name_desc(self) -> None:
        response = self.api_client.get(self.teams_url, {"ordering": "-name"})

        logger.debug("%s: %s", self._testMethodName, response.text)

        names = [t["name"] for t in response.json()["results"]]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_list_ordering_by_founded_year(self) -> None:
        response = self.api_client.get(self.teams_url, {"ordering": "founded_year"})

        logger.debug("%s: %s", self._testMethodName, response.text)

        years = [t["founded_year"] for t in response.json()["results"]]
        self.assertEqual(years, sorted(years))
