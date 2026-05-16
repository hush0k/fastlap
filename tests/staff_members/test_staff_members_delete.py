from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.team_stuff.models import StaffMember
from tests.config import TEST_LOGGER_NAME
from tests.utils import get_user

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


class TestStaffMemberDelete(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.user = get_user()
        cls.user_token = str(AccessToken.for_user(cls.user))
        cls.staff_user = get_user(
            email="staff@example.com", username="staff", is_staff=True
        )
        cls.staff_token = str(AccessToken.for_user(cls.staff_user))

    def setUp(self) -> None:
        self.member = create_staff_member()
        self.url = reverse("staff-detail", kwargs={"slug": self.member.slug})

    def test_delete_success(self) -> None:
        response = self.api_client.delete(
            self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(StaffMember.objects.filter(pk=self.member.pk).exists())

    def test_delete_unauthenticated_not_allowed(self) -> None:
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

    def test_delete_nonexistent_member(self) -> None:
        url = reverse("staff-detail", kwargs={"slug": "nonexistent-slug"})
        response = self.api_client.delete(
            url,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)
