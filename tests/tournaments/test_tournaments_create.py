from decimal import Decimal
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


class TestTournamentCreate(TestCase):
    tournaments_url = reverse("tournaments-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.user = get_user()
        cls.user_token = AccessToken.for_user(cls.user)

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
        self.valid_data = {
            "name": "Saudi Arabian Grand Prix 2025",
            "description": "Night race on the Jeddah Corniche Circuit",
            "series": self.series_f1.id,
            "year": 2025,
            "status": "finished",
            "is_active": True,
            "start_date": "2025-03-21",
            "end_date": "2025-03-23",
            "total_rounds": 50,
            "prize_fund": 2000000,
            "currency": "USD",
            "regulations_url": "https://formula1.com/regulations/saudi-2025",
            "logo": get_simple_upload_file(IMAGE_PATH),
        }

    def test_create_success(self) -> None:
        response = self.api_client.post(
            self.tournaments_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.moderator_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        tournament = Tournament.objects.get(name=self.valid_data["name"])

        self.assertEqual(tournament.description, self.valid_data["description"])
        self.assertEqual(tournament.series_id, self.valid_data["series"])
        self.assertEqual(tournament.year, self.valid_data["year"])
        self.assertEqual(tournament.status, self.valid_data["status"])
        self.assertTrue(tournament.is_active)
        self.assertEqual(str(tournament.start_date), self.valid_data["start_date"])
        self.assertEqual(str(tournament.end_date), self.valid_data["end_date"])
        self.assertEqual(tournament.total_rounds, self.valid_data["total_rounds"])
        self.assertEqual(
            tournament.prize_fund, Decimal(str(self.valid_data["prize_fund"]))
        )
        self.assertEqual(tournament.currency, self.valid_data["currency"])
        self.assertEqual(tournament.regulations_url, self.valid_data["regulations_url"])
        self.assertTrue(tournament.logo)

    def test_create_unathenticated_user_not_allowed(self) -> None:
        response = self.api_client.post(self.tournaments_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_create_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.post(
            self.tournaments_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_create_with_too_long_name(self) -> None:
        self.valid_data["name"] = "a" * 256
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="name",
            token=self.moderator_token,
        )

    def test_create_with_too_long_description(self) -> None:
        self.valid_data["description"] = "a" * 10_000
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="description",
            token=self.moderator_token,
        )

    def test_create_with_nonexistent_series(self) -> None:
        self.valid_data["series"] = 999
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="series",
            token=self.moderator_token,
        )

    def test_create_with_invalid_year(self) -> None:
        self.valid_data["year"] = -1
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="year",
            token=self.moderator_token,
        )
        self.valid_data["year"] = 32768
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="year",
            token=self.moderator_token,
        )

    def test_create_with_invalid_status(self) -> None:
        self.valid_data["status"] = "invalid"
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="status",
            token=self.moderator_token,
        )

    def test_create_with_invalid_format_of_start_date_and_end_date(self) -> None:
        self.valid_data["start_date"] = "21/03/2025"
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="start_date",
            token=self.moderator_token,
        )
        self.valid_data["end_date"] = "03/04/2025"
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="end_date",
            token=self.moderator_token,
        )

    def test_create_with_invalid_total_rounds(self) -> None:
        self.valid_data["total_rounds"] = -1
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="total_rounds",
            token=self.moderator_token,
        )
        self.valid_data["total_rounds"] = 32768
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="total_rounds",
            token=self.moderator_token,
        )

    def test_create_with_invalid_prize_fund(self) -> None:
        self.valid_data["prize_fund"] = "10000000000.00"
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="prize_fund",
            token=self.moderator_token,
        )

    def test_create_with_invalid_currency(self) -> None:
        self.valid_data["currency"] = "INVALID"
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="currency",
            token=self.moderator_token,
        )
        self.valid_data["currency"] = "ABC"
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="currency",
            token=self.moderator_token,
        )

    def test_create_with_invalid_regulations_url(self) -> None:
        self.valid_data["regulations_url"] = "INVALID"
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="regulations_url",
            token=self.moderator_token,
        )
        self.valid_data["regulations_url"] = (
            "https://formula1.com/regulations/saudi-2025-" + "a" * 255
        )
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="regulations_url",
            token=self.moderator_token,
        )

    def test_create_with_large_logo(self) -> None:
        self.valid_data["logo"] = get_simple_upload_file(LARGE_PHOTO)
        assert_validation_error(
            self=self,
            method="post",
            url=self.tournaments_url,
            data=self.valid_data,
            field="logo",
            token=self.moderator_token,
        )
