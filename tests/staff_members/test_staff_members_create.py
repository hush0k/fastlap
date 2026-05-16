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
        "first_name": "John",
        "last_name": "Smith",
        "age": 35,
        "country": "GB",
        "role": "Engineer",
    }
    defaults.update(kwargs)
    return StaffMember.objects.create(**defaults)


class TestStaffMemberCreate(TestCase):
    list_url = reverse("staff-list")

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
        self.valid_data = {
            "first_name": "John",
            "last_name": "Smith",
            "age": 35,
            "country": "GB",
            "role": "Chief Engineer",
            "description": "Experienced engineer",
            "photo": get_simple_upload_file(IMAGE_PATH),
        }

    def test_create_success(self) -> None:
        response = self.api_client.post(
            self.list_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        member = StaffMember.objects.get(first_name="John", last_name="Smith")
        self.assertEqual(member.age, self.valid_data["age"])
        self.assertEqual(member.country.code, self.valid_data["country"])
        self.assertEqual(member.role, self.valid_data["role"])
        self.assertEqual(member.description, self.valid_data["description"])
        self.assertTrue(member.photo)

    def test_create_unauthenticated_not_allowed(self) -> None:
        response = self.api_client.post(self.list_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_create_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.post(
            self.list_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_create_with_too_long_first_name(self) -> None:
        self.valid_data["first_name"] = "a" * 101
        assert_validation_error(
            self=self,
            method="post",
            url=self.list_url,
            data=self.valid_data,
            field="first_name",
            token=self.staff_token,
        )

    def test_create_with_too_long_last_name(self) -> None:
        self.valid_data["last_name"] = "a" * 101
        assert_validation_error(
            self=self,
            method="post",
            url=self.list_url,
            data=self.valid_data,
            field="last_name",
            token=self.staff_token,
        )

    def test_create_with_too_long_role(self) -> None:
        self.valid_data["role"] = "a" * 101
        assert_validation_error(
            self=self,
            method="post",
            url=self.list_url,
            data=self.valid_data,
            field="role",
            token=self.staff_token,
        )

    def test_create_with_age_below_minimum(self) -> None:
        self.valid_data["age"] = 15
        assert_validation_error(
            self=self,
            method="post",
            url=self.list_url,
            data=self.valid_data,
            field="age",
            token=self.staff_token,
        )

    def test_create_with_age_above_maximum(self) -> None:
        self.valid_data["age"] = 81
        assert_validation_error(
            self=self,
            method="post",
            url=self.list_url,
            data=self.valid_data,
            field="age",
            token=self.staff_token,
        )

    def test_create_with_invalid_country(self) -> None:
        self.valid_data["country"] = "INVALID"
        assert_validation_error(
            self=self,
            method="post",
            url=self.list_url,
            data=self.valid_data,
            field="country",
            token=self.staff_token,
        )

    def test_create_with_large_photo(self) -> None:
        self.valid_data["photo"] = get_simple_upload_file(LARGE_PHOTO)
        assert_validation_error(
            self=self,
            method="post",
            url=self.list_url,
            data=self.valid_data,
            field="photo",
            token=self.staff_token,
        )
