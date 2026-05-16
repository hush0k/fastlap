from datetime import date
from decimal import Decimal
from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.common.enums import Currency, RaceStatusEnum, SeriesCategoryEnum
from apps.races.models import Series
from apps.tournaments.models import Tournament
from tests.config import TEST_LOGGER_NAME
from tests.utils import get_user

logger = getLogger(TEST_LOGGER_NAME)


class TestTournamentsList(TestCase):
    tournaments_url = reverse("tournaments-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.user = get_user()
        cls.user_token = AccessToken.for_user(cls.user)
        cls.series_f1 = Series.objects.create(
            name="Formula 1",
            category=SeriesCategoryEnum.CAR,
        )
        cls.series_nascar = Series.objects.create(
            name="NASCAR",
            category=SeriesCategoryEnum.CAR,
        )

        cls.series_moto_gp = Series.objects.create(
            name="Moto GP",
            category=SeriesCategoryEnum.MOTO,
        )

        tournaments = [
            Tournament(
                series=cls.series_f1,
                name="Formula 1 World Championship 2023",
                year=2023,
                status=RaceStatusEnum.FINISHED,
                is_active=True,
                description="F1 season 2023.",
                start_date=date(2023, 3, 5),
                end_date=date(2023, 11, 26),
                total_rounds=22,
                prize_fund=Decimal("1500000.00"),
                currency=Currency.USD.code,
            ),
            Tournament(
                series=cls.series_f1,
                name="Formula 1 World Championship 2024",
                year=2024,
                status=RaceStatusEnum.FINISHED,
                is_active=False,
                description="F1 season 2024.",
                start_date=date(2024, 3, 2),
                end_date=date(2024, 12, 8),
                total_rounds=24,
                prize_fund=Decimal("1700000.00"),
                currency=Currency.USD.code,
            ),
            Tournament(
                series=cls.series_f1,
                name="Formula 1 World Championship 2025",
                year=2025,
                status=RaceStatusEnum.LIVE,
                is_active=True,
                description="F1 season 2025.",
                start_date=date(2025, 3, 16),
                end_date=date(2025, 12, 7),
                total_rounds=24,
                prize_fund=Decimal("1800000.00"),
                currency=Currency.USD.code,
            ),
            Tournament(
                series=cls.series_f1,
                name="Formula 1 World Championship 2026",
                year=2026,
                status=RaceStatusEnum.UPCOMING,
                is_active=True,
                description="",
                start_date=date(2026, 3, 1),
                end_date=date(2026, 11, 29),
                total_rounds=23,
                prize_fund=None,
                currency=Currency.USD.code,
            ),
            Tournament(
                series=cls.series_nascar,
                name="NASCAR Cup Series 2023",
                year=2023,
                status=RaceStatusEnum.FINISHED,
                is_active=False,
                description="NASCAR Cup season 2023.",
                start_date=date(2023, 2, 5),
                end_date=date(2023, 11, 5),
                total_rounds=36,
                prize_fund=Decimal("800000.00"),
                currency=Currency.USD.code,
            ),
            Tournament(
                series=cls.series_nascar,
                name="NASCAR Cup Series 2024",
                year=2024,
                status=RaceStatusEnum.FINISHED,
                is_active=True,
                description="NASCAR Cup season 2024.",
                start_date=date(2024, 2, 18),
                end_date=date(2024, 11, 10),
                total_rounds=36,
                prize_fund=Decimal("850000.00"),
                currency=Currency.USD.code,
            ),
            Tournament(
                series=cls.series_nascar,
                name="NASCAR Cup Series 2025",
                year=2025,
                status=RaceStatusEnum.LIVE,
                is_active=True,
                description="",
                start_date=date(2025, 2, 2),
                end_date=date(2025, 11, 9),
                total_rounds=36,
                prize_fund=Decimal("900000.00"),
                currency=Currency.USD.code,
            ),
            Tournament(
                series=cls.series_moto_gp,
                name="MotoGP World Championship 2023",
                year=2023,
                status=RaceStatusEnum.FINISHED,
                is_active=True,
                description="MotoGP season 2023.",
                start_date=date(2023, 3, 26),
                end_date=date(2023, 11, 26),
                total_rounds=20,
                prize_fund=Decimal("600000.00"),
                currency=Currency.EUR.code,
            ),
            Tournament(
                series=cls.series_moto_gp,
                name="MotoGP World Championship 2024",
                year=2024,
                status=RaceStatusEnum.FINISHED,
                is_active=True,
                description="MotoGP season 2024.",
                start_date=date(2024, 3, 10),
                end_date=date(2024, 11, 17),
                total_rounds=20,
                prize_fund=Decimal("650000.00"),
                currency=Currency.EUR.code,
            ),
            Tournament(
                series=cls.series_moto_gp,
                name="MotoGP World Championship 2025",
                year=2025,
                status=RaceStatusEnum.CANCELLED,
                is_active=True,
                description="MotoGP season 2025 cancelled.",
                start_date=date(2025, 3, 23),
                end_date=date(2025, 11, 16),
                total_rounds=20,
                prize_fund=Decimal("650000.00"),
                currency=Currency.EUR.code,
            ),
        ]

        Tournament.objects.bulk_create(tournaments)

    def setUp(self) -> None:
        pass

    def test_list_all(self) -> None:
        response = self.client.get(self.tournaments_url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 8)

    def test_filter_with_slug(self) -> None:
        torunament = Tournament.objects.filter(
            name="Formula 1 World Championship 2026"
        ).first()
        response = self.api_client.get(self.tournaments_url, {"slug": torunament.slug})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["name"], torunament.name)

    def test_filter_with_max_prize(self) -> None:
        prize = 800000
        response = self.api_client.get(self.tournaments_url, {"max_prize": prize})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 3)
        for t in response.json()["results"]:
            self.assertLessEqual(float(t["prize_fund"]), prize)

    def test_filter_with_min_prize(self) -> None:
        prize = 800000
        response = self.api_client.get(self.tournaments_url, {"min_prize": prize})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 4)
        for t in response.json()["results"]:
            self.assertGreaterEqual(float(t["prize_fund"]), prize)

    def test_filter_by_series(self) -> None:
        response = self.api_client.get(
            self.tournaments_url, {"series": self.series_nascar.name}
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 2)
        for t in response.json()["results"]:
            self.assertEqual(t["series"]["name"], self.series_nascar.name)

    def test_filter_by_year(self) -> None:
        response = self.api_client.get(self.tournaments_url, {"year": 2024})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 2)
        for t in response.json()["results"]:
            self.assertEqual(t["year"], 2024)

    def test_filter_before(self) -> None:
        response = self.api_client.get(self.tournaments_url, {"before": 2024})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 2)
        for t in response.json()["results"]:
            self.assertLess(t["year"], 2024)

    def test_filter_after(self) -> None:
        response = self.api_client.get(self.tournaments_url, {"after": 2024})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 4)
        for t in response.json()["results"]:
            self.assertGreater(t["year"], 2024)

    def test_filter_by_status(self) -> None:
        response = self.api_client.get(
            self.tournaments_url, {"status": RaceStatusEnum.LIVE}
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 2)
        self.assertEqual(response.json()["results"][0]["status"], RaceStatusEnum.LIVE)
        self.assertEqual(response.json()["results"][1]["status"], RaceStatusEnum.LIVE)

    def test_filter_with_min_rounds(self) -> None:
        response = self.api_client.get(self.tournaments_url, {"min_rounds": 20})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 8)

    def test_filter_with_max_rounds(self) -> None:
        response = self.api_client.get(self.tournaments_url, {"max_rounds": 30})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 6)

    def test_filter_by_before_date(self) -> None:
        date_str = date(2025, 3, 23).isoformat()
        response = self.api_client.get(self.tournaments_url, {"before_date": date_str})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 6)
        for t in response.json()["results"]:
            self.assertLess(t["start_date"], date_str)

    def test_filter_by_after_date(self) -> None:
        date_str = date(2025, 3, 23).isoformat()
        response = self.api_client.get(self.tournaments_url, {"after_date": date_str})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.json()["count"], 1)
        self.assertGreater(response.json()["results"][0]["start_date"], date_str)

    def test_search_by_name(self) -> None:
        response = self.api_client.get(self.tournaments_url, {"search": "Formula 1"})
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 3)

        for t in response.json()["results"]:
            self.assertIn("Formula 1", t["name"])
