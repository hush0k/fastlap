from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.models import Group
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.common.enums import RoleEnum, SeriesCategoryEnum
from apps.races.models import Series
from apps.tournaments.models import Tournament
from tests.config import IMAGE_PATH, LARGE_PHOTO, TEST_LOGGER_NAME
from tests.utils import assert_validation_error, get_simple_upload_file, get_user

logger = getLogger(TEST_LOGGER_NAME)


class TestTournamentUpdate(TestCase):

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
        cls.series_motogp = Series.objects.create(
            name="MotoGP",
            category=SeriesCategoryEnum.MOTO,
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

    def test_update_success(self) -> None:
        data = {
            "name": "Updated Grand Prix 2025",
            "description": "Updated description",
            "series": self.series_motogp.id,
            "year": 2026,
            "status": "upcoming",
            "is_active": False,
            "start_date": "2026-04-01",
            "end_date": "2026-04-03",
            "total_rounds": 60,
            "logo": get_simple_upload_file(IMAGE_PATH),
        }
        response = self.api_client.patch(
            self.url,
            data,
            HTTP_AUTHORIZATION=f"Bearer {self.moderator_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.tournament.refresh_from_db()

        self.assertEqual(self.tournament.name, data["name"])
        self.assertEqual(self.tournament.description, data["description"])
        self.assertEqual(self.tournament.series_id, data["series"])
        self.assertEqual(self.tournament.year, data["year"])
        self.assertEqual(self.tournament.status, data["status"])
        self.assertFalse(self.tournament.is_active)
        self.assertEqual(str(self.tournament.start_date), data["start_date"])
        self.assertEqual(str(self.tournament.end_date), data["end_date"])
        self.assertEqual(self.tournament.total_rounds, data["total_rounds"])
        self.assertTrue(self.tournament.logo)

    def test_update_partial_success(self) -> None:
        response = self.api_client.patch(
            self.url,
            {"name": "Only Name Changed"},
            HTTP_AUTHORIZATION=f"Bearer {self.moderator_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.name, "Only Name Changed")
        self.assertEqual(self.tournament.year, 2025)

    def test_update_unauthenticated_user_not_allowed(self) -> None:
        response = self.api_client.patch(self.url, {"name": "New Name"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_update_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.patch(
            self.url,
            {"name": "New Name"},
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_update_nonexistent_tournament(self) -> None:
        url = reverse("tournaments-detail", kwargs={"slug": "nonexistent-slug"})
        response = self.api_client.patch(
            url,
            {"name": "New Name"},
            HTTP_AUTHORIZATION=f"Bearer {self.moderator_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)

    def test_update_with_too_long_name(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"name": "a" * 256},
            field="name",
            token=self.moderator_token,
        )

    def test_update_with_too_long_description(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"description": "a" * 10_000},
            field="description",
            token=self.moderator_token,
        )

    def test_update_with_nonexistent_series(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"series": 999},
            field="series",
            token=self.moderator_token,
        )

    def test_update_with_invalid_year(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"year": -1},
            field="year",
            token=self.moderator_token,
        )
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"year": 32768},
            field="year",
            token=self.moderator_token,
        )

    def test_update_with_invalid_status(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"status": "invalid"},
            field="status",
            token=self.moderator_token,
        )

    def test_update_with_invalid_format_of_start_date(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"start_date": "21/03/2025"},
            field="start_date",
            token=self.moderator_token,
        )

    def test_update_with_invalid_format_of_end_date(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"end_date": "23/03/2025"},
            field="end_date",
            token=self.moderator_token,
        )

    def test_update_with_invalid_total_rounds(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"total_rounds": -1},
            field="total_rounds",
            token=self.moderator_token,
        )
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"total_rounds": 32768},
            field="total_rounds",
            token=self.moderator_token,
        )

    def test_update_with_large_logo(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"logo": get_simple_upload_file(LARGE_PHOTO)},
            field="logo",
            token=self.moderator_token,
        )
