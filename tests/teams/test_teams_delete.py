from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.teams.models import Team
from tests.config import TEST_LOGGER_NAME
from tests.utils import get_user

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


class TestTeamDelete(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)
        cls.user_token = str(AccessToken.for_user(cls.user))
        cls.staff_token = str(AccessToken.for_user(cls.staff))

    def setUp(self) -> None:
        self.team = create_team(name="Delete Team", short_name="DEL")
        self.url = reverse("teams-detail", kwargs={"slug": self.team.slug})

    def test_delete_success(self) -> None:
        response = self.api_client.delete(
            self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Team.objects.filter(id=self.team.id).exists())

    def test_delete_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.delete(self.url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 401)
        self.assertTrue(Team.objects.filter(id=self.team.id).exists())

    def test_delete_by_odrinary_user_not_allowed(self) -> None:
        response = self.api_client.delete(
            self.url, HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Team.objects.filter(id=self.team.id).exists())

    def test_delete_nonexistent_team_returns_404(self) -> None:
        url = reverse("teams-detail", kwargs={"slug": "nonexistent-slug"})
        response = self.api_client.delete(
            url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 404)
