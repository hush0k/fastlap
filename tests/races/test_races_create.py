from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.common.enums import RaceStatusEnum, WatchPlatformEnum
from apps.races.models import Race, Series
from tests.config import TEST_LOGGER_NAME
from tests.utils import assert_validation_error, get_user

logger = getLogger(TEST_LOGGER_NAME)


class TestRaceCreate(TestCase):
    races_url = reverse("races-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()

        cls.user = get_user()

        cls.staff = get_user(
            email="staff@example.com",
            username="staff",
            is_staff=True,
        )

        cls.user_token = str(AccessToken.for_user(cls.user))
        cls.staff_token = str(AccessToken.for_user(cls.staff))

        cls.series = Series.objects.create(
            name="Formula 1",
            category="car",
        )

    def setUp(self) -> None:
        self.valid_data = {
            "name": "Monaco Grand Prix",
            "series": self.series.id,
            "round_number": 8,
            "scheduled_at": "2025-06-01T14:00:00Z",
            "status": RaceStatusEnum.UPCOMING,
            "watch_platform": WatchPlatformEnum.F1_TV,
        }

    def test_success_create(self) -> None:
        response = self.api_client.post(
            self.races_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Race.objects.filter(
                name=response.json()["name"],
            ).exists()
        )

        race = Race.objects.get(
            name=response.json()["name"],
        )

        self.assertEqual(
            race.name,
            self.valid_data["name"],
        )

        self.assertEqual(
            race.round_number,
            self.valid_data["round_number"],
        )

        self.assertEqual(
            race.status,
            self.valid_data["status"],
        )

    def test_create_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.post(
            self.races_url,
            self.valid_data,
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 401)

    def test_create_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.post(
            self.races_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 403)

    def test_create_without_required_fields(self) -> None:
        required_fields = [
            "name",
            "series",
            "round_number",
            "scheduled_at",
            "status",
            "watch_platform",
        ]

        for field in required_fields:
            data = {k: v for k, v in self.valid_data.items() if k != field}

            assert_validation_error(
                api_client=self.api_client,
                method="post",
                url=self.races_url,
                data=data,
                field=field,
                token=self.staff_token,
                logger=logger,
                test_name=self._testMethodName,
            )

    def test_create_with_empty_name(self) -> None:
        assert_validation_error(
            api_client=self.api_client,
            method="post",
            url=self.races_url,
            data=self.valid_data | {"name": "   "},
            field="name",
            token=self.staff_token,
            logger=logger,
            test_name=self._testMethodName,
        )

    def test_create_with_invalid_status(self) -> None:
        assert_validation_error(
            api_client=self.api_client,
            method="post",
            url=self.races_url,
            data=self.valid_data | {"status": "invalid"},
            field="status",
            token=self.staff_token,
            logger=logger,
            test_name=self._testMethodName,
        )

    def test_create_with_invalid_watch_platform(self) -> None:
        assert_validation_error(
            api_client=self.api_client,
            method="post",
            url=self.races_url,
            data=self.valid_data | {"watch_platform": "invalid"},
            field="watch_platform",
            token=self.staff_token,
            logger=logger,
            test_name=self._testMethodName,
        )

    def test_create_with_invalid_round_number(self) -> None:
        for value in [0, -1]:
            assert_validation_error(
                api_client=self.api_client,
                method="post",
                url=self.races_url,
                data=self.valid_data | {"round_number": value},
                field="round_number",
                token=self.staff_token,
                logger=logger,
                test_name=self._testMethodName,
            )

    def test_create_with_invalid_laps_total(self) -> None:
        for value in [0, -1]:
            assert_validation_error(
                api_client=self.api_client,
                method="post",
                url=self.races_url,
                data=self.valid_data | {"laps_total": value},
                field="laps_total",
                token=self.staff_token,
                logger=logger,
                test_name=self._testMethodName,
            )

    def test_create_with_invalid_watch_url(self) -> None:
        assert_validation_error(
            api_client=self.api_client,
            method="post",
            url=self.races_url,
            data=self.valid_data | {"watch_url": "not-a-url"},
            field="watch_url",
            token=self.staff_token,
            logger=logger,
            test_name=self._testMethodName,
        )

    def test_create_with_nonexistent_series(self) -> None:
        assert_validation_error(
            api_client=self.api_client,
            method="post",
            url=self.races_url,
            data=self.valid_data | {"series": 999999},
            field="series",
            token=self.staff_token,
            logger=logger,
            test_name=self._testMethodName,
        )
