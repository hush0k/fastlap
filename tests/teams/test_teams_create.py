from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.teams.models import Team
from tests.config import IMAGE_PATH, TEST_LOGGER_NAME
from tests.utils import assert_validation_error, get_simple_upload_file, get_user

logger = getLogger(TEST_LOGGER_NAME)


def create_team(**kwargs) -> Team:
    data = dict(
        name="Test Team",
        short_name="TST",
        country="US",
        founded_year=2000,
    )
    data.update(**kwargs)
    return Team.objects.create(**data)


class TestTeamCreate(TestCase):
    teams_url = reverse("teams-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)
        cls.user_token = str(AccessToken.for_user(cls.user))
        cls.staff_token = str(AccessToken.for_user(cls.staff))

    def setUp(self) -> None:
        self.valid_data = {
            "name": "Red Bull Racing",
            "short_name": "RBR",
            "country": "AT",
            "founded_year": 2005,
            "description": "A professional racing team.",
            "budget": "500000000.00",
            "budget_currency": "USD",
            "main_sponsor": "Oracle",
            "secondary_sponsor": "AlphaTauri",
        }

    def test_success_create(self) -> None:
        response = self.api_client.post(
            self.teams_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)

        team = Team.objects.get(name=self.valid_data["name"])
        self.assertEqual(team.short_name, self.valid_data["short_name"])
        self.assertEqual(str(team.country), self.valid_data["country"])
        self.assertEqual(team.founded_year, self.valid_data["founded_year"])
        self.assertEqual(team.description, self.valid_data["description"])
        self.assertEqual(str(team.budget), self.valid_data["budget"])
        self.assertEqual(team.budget_currency, self.valid_data["budget_currency"])
        self.assertEqual(team.main_sponsor, self.valid_data["main_sponsor"])
        self.assertEqual(team.secondary_sponsor, self.valid_data["secondary_sponsor"])

    def test_success_create_with_logo(self) -> None:
        response = self.api_client.post(
            self.teams_url,
            self.valid_data | {"logo": get_simple_upload_file(IMAGE_PATH)},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)
        team = Team.objects.get(name=self.valid_data["name"])
        self.assertTrue(bool(team.logo))

    def test_success_create_with_banner(self) -> None:
        response = self.api_client.post(
            self.teams_url,
            self.valid_data | {"banner": get_simple_upload_file(IMAGE_PATH)},
            format="multipart",
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)
        team = Team.objects.get(name=self.valid_data["name"])
        self.assertTrue(bool(team.banner))

    def test_create_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.post(self.teams_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_create_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.post(
            self.teams_url,
            self.valid_data,
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_create_without_required_fields(self) -> None:
        required_fields = ["name", "short_name"]

        for field in required_fields:
            data = {k: v for k, v in self.valid_data.items() if k != field}
            assert_validation_error(
                self=self,
                method="post",
                url=self.teams_url,
                data=data,
                field=field,
                token=self.staff_token,
            )

    def test_create_optional_fields_can_be_omitted(self) -> None:
        data = {"name": "Minimal Team", "short_name": "MIN", "country": "AT"}

        response = self.api_client.post(
            self.teams_url, data, HTTP_AUTHORIZATION=f"Bearer {self.staff_token}"
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 201)

    def test_create_with_invalid_budget_currency_length(self) -> None:
        for value in ["US", "EURO"]:
            assert_validation_error(
                self=self,
                method="post",
                url=self.teams_url,
                data=self.valid_data | {"budget_currency": value},
                field="budget_currency",
                token=self.staff_token,
            )

    def test_create_budget_currency_is_uppercased(self) -> None:
        response = self.api_client.post(
            self.teams_url,
            self.valid_data | {"budget_currency": "eur"},
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)
        team = Team.objects.get(name=self.valid_data["name"])
        self.assertEqual(team.budget_currency, "EUR")

    def test_create_with_invalid_country_code(self) -> None:
        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data | {"country": "INVALID"},
            field="country",
            token=self.staff_token,
        )

    def test_create_with_empty_logo_file(self) -> None:
        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data
            | {"logo": get_simple_upload_file(IMAGE_PATH, empty=True)},
            field="logo",
            token=self.staff_token,
        )

    def test_create_with_empty_banner_file(self) -> None:
        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data
            | {"banner": get_simple_upload_file(IMAGE_PATH, empty=True)},
            field="banner",
            token=self.staff_token,
        )

    def test_create_with_duplicate_name_not_allowed(self) -> None:
        create_team(name="Red Bull Racing")

        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data | {"name": "Red Bull Racing"},
            field="name",
            token=self.staff_token,
        )

    def test_create_with_duplicate_short_name_not_allowed(self) -> None:
        create_team(short_name="RBR")

        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data | {"short_name": "RBR"},
            field="short_name",
            token=self.staff_token,
        )

    def test_create_with_name_exceeding_max_length(self) -> None:
        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data | {"name": "A" * 256},
            field="name",
            token=self.staff_token,
        )

    def test_create_with_short_name_exceeding_max_length(self) -> None:
        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data | {"short_name": "LONGSHORTNAME"},
            field="short_name",
            token=self.staff_token,
        )

    def test_create_with_founded_year_exceeding_integer_limit(self) -> None:
        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data | {"founded_year": 32768},
            field="founded_year",
            token=self.staff_token,
        )

    def test_create_with_budget_exceeding_max_digits(self) -> None:
        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data | {"budget": "10000000000000.00"},
            field="budget",
            token=self.staff_token,
        )

    def test_create_with_blank_strings_for_optional_fields(self) -> None:
        data = self.valid_data | {
            "description": "",
            "main_sponsor": "",
            "secondary_sponsor": "",
            "budget_currency": "",
        }
        response = self.api_client.post(
            self.teams_url,
            data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 201)

        team = Team.objects.get(name=self.valid_data["name"])
        self.assertEqual(team.budget_currency, "")

    def test_create_with_invalid_logo_file_type(self) -> None:
        invalid_file = SimpleUploadedFile(
            "test.txt", b"not_an_image_content", content_type="text/plain"
        )
        assert_validation_error(
            self=self,
            method="post",
            url=self.teams_url,
            data=self.valid_data | {"logo": invalid_file},
            field="logo",
            token=self.staff_token,
        )
