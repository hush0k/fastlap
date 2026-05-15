from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.drivers.models import Driver
from tests.config import TEST_LOGGER_NAME
from tests.utils import get_user

logger = getLogger(TEST_LOGGER_NAME)


class TestArtcilesList(TestCase):
    drivers_url = reverse("drivers-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()

        drivers = [
            Driver(
                first_name="Max",
                last_name="Verstappen",
                nationality="NL",
                date_of_birth="1997-09-30",
                number=1,
                bio="Multiple World Champion known for aggressive racecraft and dominant pace.",
                is_active=True,
            ),
            Driver(
                first_name="Lewis",
                last_name="Hamilton",
                nationality="GB",
                date_of_birth="1985-01-07",
                number=44,
                bio="Seven-time World Champion with elite consistency and race management.",
                is_active=True,
            ),
            Driver(
                first_name="Charles",
                last_name="Leclerc",
                nationality="MC",
                date_of_birth="1997-10-16",
                number=16,
                bio="Strong qualifier with explosive single-lap speed.",
                is_active=True,
            ),
            Driver(
                first_name="Lando",
                last_name="Norris",
                nationality="GB",
                date_of_birth="1999-11-13",
                number=4,
                bio="Consistent and adaptable driver with strong race craft.",
                is_active=True,
            ),
            Driver(
                first_name="Fernando",
                last_name="Alonso",
                nationality="ES",
                date_of_birth="1981-07-29",
                number=14,
                bio="Veteran two-time World Champion with elite race intelligence.",
                is_active=True,
            ),
            Driver(
                first_name="George",
                last_name="Russell",
                nationality="GB",
                date_of_birth="1998-02-15",
                number=63,
                bio="Technically precise driver with strong qualifying performance.",
                is_active=False,
            ),
        ]

        Driver.objects.bulk_create(drivers)

        cls.user = get_user()
        cls.access = AccessToken.for_user(cls.user)

    def test_success_list(self) -> None:
        response = self.api_client.get(
            self.drivers_url, HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 6)

    def test_unauthenticated_not_allowed(self) -> None:
        response = self.api_client.get(self.drivers_url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 401)

    def test_filter_nationality(self) -> None:
        response = self.api_client.get(
            self.drivers_url + "?nationality=NL",
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 1)

    def test_filter_search_by_first_name(self) -> None:
        response = self.api_client.get(
            self.drivers_url + "?search=Max",
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["last_name"], "Verstappen")

    def test_filter_search_by_last_name(self) -> None:
        response = self.api_client.get(
            self.drivers_url + "?search=Verstappen",
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["first_name"], "Max")

    def test_filter_is_active(self) -> None:
        response = self.api_client.get(
            self.drivers_url + "?is_active=false",
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 1)

    def test_filter_number(self) -> None:
        response = self.api_client.get(
            self.drivers_url + "?number=14",
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["last_name"], "Alonso")
