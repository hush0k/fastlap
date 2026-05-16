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


class TestRaceUpdate(TestCase):
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
        self.race = Race.objects.create(
            name="Monaco Grand Prix",
            series=self.series,
            round_number=8,
            scheduled_at="2025-06-01T14:00:00Z",
            status=RaceStatusEnum.UPCOMING,
            watch_platform=WatchPlatformEnum.F1_TV,
        )

        self.race_url = reverse(
            "races-detail",
            kwargs={"slug": self.race.slug},
        )

        self.valid_data = {
            "name": "Monaco Grand Prix",
            "series": self.series.id,
            "round_number": 8,
            "scheduled_at": "2025-06-01T14:00:00Z",
            "status": RaceStatusEnum.UPCOMING,
            "watch_platform": WatchPlatformEnum.F1_TV,
            "watch_url": "https://f1tv.formula1.com/monaco",
        }

    def test_success_full_update(self) -> None:
        response = self.api_client.put(
            self.race_url,
            self.valid_data
            | {
                "name": "British Grand Prix",
                "round_number": 12,
                "status": RaceStatusEnum.FINISHED,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)

        self.race.refresh_from_db()

        self.assertEqual(self.race.name, "British Grand Prix")
        self.assertEqual(self.race.round_number, 12)
        self.assertEqual(self.race.status, RaceStatusEnum.FINISHED)

    def test_success_partial_update(self) -> None:
        partial_updates = [
            {"name": "British Grand Prix"},
            {"status": RaceStatusEnum.FINISHED},
            {"round_number": 12},
            {"watch_platform": WatchPlatformEnum.DAZN},
            {"laps_total": 78},
        ]

        for data in partial_updates:
            response = self.api_client.patch(
                self.race_url,
                data,
                HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
            )

            logger.debug(
                "%s %s: %s",
                self._testMethodName,
                data,
                response.text,
            )

            self.assertEqual(response.status_code, 200)
            self.race.refresh_from_db()

            field, value = next(iter(data.items()))

            self.assertEqual(
                getattr(self.race, field),
                value,
            )

    def test_update_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.put(
            self.race_url,
            self.valid_data,
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 401)

    def test_update_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.put(
            self.race_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 403)

    def test_full_update_without_required_fields(self) -> None:
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
                self=self,
                method="put",
                url=self.race_url,
                data=data,
                field=field,
                token=self.staff_token,
            )

    def test_update_with_empty_name(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.race_url,
            data={"name": "   "},
            field="name",
            token=self.staff_token,
        )

    def test_update_with_invalid_status(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.race_url,
            data={"status": "invalid"},
            field="status",
            token=self.staff_token,
        )

    def test_update_with_invalid_round_number(self) -> None:
        for value in [0, -1]:
            assert_validation_error(
                self=self,
                method="patch",
                url=self.race_url,
                data={"round_number": value},
                field="round_number",
                token=self.staff_token,
            )

    def test_update_nonexistent_race(self) -> None:
        response = self.api_client.patch(
            reverse(
                "races-detail",
                kwargs={"slug": "nonexistent-race"},
            ),
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 404)

    def test_update_with_invalid_watch_url(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.race_url,
            data={"watch_url": "not-a-url"},
            field="watch_url",
            token=self.staff_token,
        )

    def test_update_with_watch_url_too_long(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.race_url,
            data={
                "watch_url": "https://example.com/" + "a" * 260,
            },
            field="watch_url",
            token=self.staff_token,
        )

    def test_update_with_invalid_laps_total(self) -> None:
        for value in [0, -1]:
            assert_validation_error(
                self=self,
                method="patch",
                url=self.race_url,
                data={"laps_total": value},
                field="laps_total",
                token=self.staff_token,
            )

    def test_update_with_invalid_scheduled_at(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.race_url,
            data={"scheduled_at": "not-a-datetime"},
            field="scheduled_at",
            token=self.staff_token,
        )

    def test_update_with_nonexistent_series(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.race_url,
            data={"series": 999999},
            field="series",
            token=self.staff_token,
        )

    def test_update_with_invalid_watch_platform(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.race_url,
            data={"watch_platform": "invalid"},
            field="watch_platform",
            token=self.staff_token,
        )
