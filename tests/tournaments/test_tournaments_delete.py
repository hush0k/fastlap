from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.models import Group
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.common.enums import RoleEnum, SeriesCategoryEnum
from apps.races.models import Series
from apps.tournaments.models import Tournament
from tests.config import TEST_LOGGER_NAME
from tests.utils import get_user

logger = getLogger(TEST_LOGGER_NAME)


class TestTournamentDelete(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.user = get_user()
        cls.user_token = str(AccessToken.for_user(cls.user))

        content_moderator_group = Group.objects.get_or_create(
            name=RoleEnum.CONTENT_MANAGER
        )[0]
        cls.moderator = get_user(email="moderator@example.com", username="moderator")
        cls.moderator.groups.add(content_moderator_group)
        cls.moderator_token = str(AccessToken.for_user(cls.moderator))

        cls.series_f1 = Series.objects.create(
            name="Formula 1",
            category=SeriesCategoryEnum.CAR,
        )

    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(
            name="Saudi Arabian Grand Prix 2025",
            description="Night race on the Jeddah Corniche Circuit",
            series=self.series_f1,
            year=2025,
            status="finished",
            is_active=True,
            start_date="2025-03-21",
            end_date="2025-03-23",
            total_rounds=50,
        )
        self.url = reverse("tournaments-detail", kwargs={"slug": self.tournament.slug})

    def test_delete_success(self) -> None:
        response = self.api_client.delete(
            self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.moderator_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Tournament.objects.filter(pk=self.tournament.pk).exists())

    def test_delete_unauthenticated_user_not_allowed(self) -> None:
        response = self.api_client.delete(self.url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_delete_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.delete(
            self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_delete_nonexistent_tournament(self) -> None:
        url = reverse("tournaments-detail", kwargs={"slug": "nonexistent-slug"})
        response = self.api_client.delete(
            url,
            HTTP_AUTHORIZATION=f"Bearer {self.moderator_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)
