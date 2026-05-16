from logging import getLogger

from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.team_stuff.models import StaffMember, TeamRoster
from apps.teams.models import Team
from tests.config import TEST_LOGGER_NAME

logger = getLogger(TEST_LOGGER_NAME)


def create_staff_member(**kwargs) -> StaffMember:
    defaults = {
        "name": "John Smith",
        "first_name": "John",
        "last_name": "Smith",
        "age": 35,
        "country": "GB",
        "role": "Engineer",
    }
    defaults.update(kwargs)
    return StaffMember.objects.create(**defaults)


class TestStaffMemberHistory(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.member = create_staff_member()
        cls.team = Team.objects.create(name="Red Bull Racing", short_name="RBR")
        cls.url = reverse("staff-history", kwargs={"slug": cls.member.slug})

    def test_history_returns_rosters_ordered_by_start_date(self) -> None:
        TeamRoster.objects.create(
            team=self.team,
            staff_member=self.member,
            start_date="2022-01-01",
            is_active=False,
        )
        TeamRoster.objects.create(
            team=self.team,
            staff_member=self.member,
            start_date="2024-01-01",
            is_active=True,
        )
        response = self.api_client.get(self.url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertGreater(
            response.data[0]["start_date"], response.data[1]["start_date"]
        )

    def test_history_empty_rosters(self) -> None:
        response = self.api_client.get(self.url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_history_nonexistent_member(self) -> None:
        url = reverse("staff-history", kwargs={"slug": "nonexistent-slug"})
        response = self.api_client.get(url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)
