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


class TestTeamDetail(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.team = create_team(
            name="Detail Team",
            short_name="DET",
            country="DE",
            founded_year=1995,
            description="Some description",
            budget="999999.99",
            budget_currency="EUR",
            main_sponsor="Sponsor A",
            secondary_sponsor="Sponsor B",
        )
        cls.url = reverse("teams-detail", kwargs={"slug": cls.team.slug})

    def test_get_team_detail_success(self) -> None:
        response = self.api_client.get(self.url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        expected_fields = [
            "id",
            "name",
            "slug",
            "short_name",
            "logo",
            "banner",
            "country",
            "country_name",
            "founded_year",
            "description",
            "budget",
            "budget_currency",
            "main_sponsor",
            "secondary_sponsor",
            "standings",
            "created_at",
            "updated_at",
        ]
        for field in expected_fields:
            with self.subTest(check="field_presence", field=field):
                self.assertIn(field, data)

        expected_values = {
            "name": self.team.name,
            "short_name": self.team.short_name,
            "founded_year": self.team.founded_year,
            "description": self.team.description,
            "budget_currency": self.team.budget_currency,
            "main_sponsor": self.team.main_sponsor,
            "secondary_sponsor": self.team.secondary_sponsor,
        }
        for field, expected_val in expected_values.items():
            with self.subTest(check="field_value", field=field):
                self.assertEqual(data[field], expected_val)

        self.assertIsInstance(data["standings"], list)

    def test_get_team_detail_nonexistent_slug_returns_404(self) -> None:
        url = reverse("teams-detail", kwargs={"slug": "nonexistent-slug"})
        response = self.api_client.get(url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 404)
