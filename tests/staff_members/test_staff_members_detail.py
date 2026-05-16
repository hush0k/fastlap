from logging import getLogger

from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.team_stuff.models import StaffMember
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


class TestStaffMemberDetail(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.member = create_staff_member()
        cls.url = reverse("staff-detail", kwargs={"slug": cls.member.slug})

    def test_detail_success_without_auth(self) -> None:
        response = self.api_client.get(self.url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.member.id)
        self.assertEqual(response.data["first_name"], self.member.first_name)
        self.assertEqual(response.data["last_name"], self.member.last_name)
        self.assertEqual(
            response.data["full_name"],
            f"{self.member.first_name} {self.member.last_name}",
        )
        self.assertEqual(response.data["age"], self.member.age)
        self.assertEqual(response.data["country"], "United Kingdom")
        self.assertEqual(response.data["country_code"], self.member.country)
        self.assertEqual(response.data["role"], self.member.role)
        self.assertEqual(response.data["description"], "")
        self.assertEqual(response.data["photo"], None)
        self.assertEqual(response.data["rosters"], [])
        self.assertEqual(
            response.data["created_at"],
            self.member.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        self.assertEqual(
            response.data["updated_at"],
            self.member.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )

    def test_detail_nonexistent_member(self) -> None:
        url = reverse("staff-detail", kwargs={"slug": "nonexistent-slug"})
        response = self.api_client.get(url)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)
