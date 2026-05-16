from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from apps.team_stuff.models import StaffMember
from tests.config import IMAGE_PATH, LARGE_PHOTO, TEST_LOGGER_NAME
from tests.utils import assert_validation_error, get_simple_upload_file, get_user

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


class TestStaffMemberUpdate(TestCase):
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

    def test_update_success(self) -> None:
        data = {
            "first_name": "James",
            "last_name": "Doe",
            "age": 40,
            "country": "DE",
            "role": "Team Principal",
            "description": "Updated description",
            "photo": get_simple_upload_file(IMAGE_PATH),
        }

        response = self.api_client.patch(
            self.url,
            data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)

        self.member.refresh_from_db()
        self.assertEqual(self.member.first_name, data["first_name"])
        self.assertEqual(self.member.last_name, data["last_name"])
        self.assertEqual(self.member.age, data["age"])
        self.assertEqual(self.member.country.code, data["country"])
        self.assertEqual(self.member.role, data["role"])
        self.assertEqual(self.member.description, data["description"])
        self.assertTrue(self.member.photo)

    def test_update_partial_success(self) -> None:
        response = self.api_client.patch(
            self.url,
            {"role": "Race Engineer"},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.member.refresh_from_db()
        self.assertEqual(self.member.role, "Race Engineer")
        self.assertEqual(self.member.first_name, "John")

    def test_update_unauthenticated_not_allowed(self) -> None:
        response = self.api_client.patch(self.url, {"role": "Engineer"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_update_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.patch(
            self.url,
            {"role": "Engineer"},
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_update_nonexistent_member(self) -> None:
        url = reverse("staff-detail", kwargs={"slug": "nonexistent-slug"})
        response = self.api_client.patch(
            url,
            {"role": "Engineer"},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 404)

    def test_update_with_too_long_first_name(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"first_name": "a" * 101},
            field="first_name",
            token=self.staff_token,
        )

    def test_update_with_too_long_last_name(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"last_name": "a" * 101},
            field="last_name",
            token=self.staff_token,
        )

    def test_update_with_too_long_role(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"role": "a" * 101},
            field="role",
            token=self.staff_token,
        )

    def test_update_with_age_below_minimum(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"age": 15},
            field="age",
            token=self.staff_token,
        )

    def test_update_with_age_above_maximum(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"age": 81},
            field="age",
            token=self.staff_token,
        )

    def test_update_with_invalid_country(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"country": "INVALID"},
            field="country",
            token=self.staff_token,
        )

    def test_update_with_large_photo(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"photo": get_simple_upload_file(LARGE_PHOTO)},
            field="photo",
            token=self.staff_token,
        )
