from decimal import Decimal
from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

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


class TestTeamUpdate(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.api_client = APIClient()
        cls.user = get_user()
        cls.staff = get_user(email="staff@example.com", username="staff", is_staff=True)

        cls.user_token = str(AccessToken.for_user(cls.user))
        cls.staff_token = str(AccessToken.for_user(cls.staff))

    def setUp(self) -> None:
        self.team = create_team(
            name="Update Team",
            short_name="UPD",
            country="US",
            founded_year=2000,
            description="Old description",
            budget_currency="USD",
            main_sponsor="Old Sponsor",
            secondary_sponsor="Old Secondary",
        )
        self.url = reverse("teams-detail", kwargs={"slug": self.team.slug})

    from decimal import Decimal

    # ...

    def test_partial_updates(self) -> None:
        cases = [
            ("name", "New Name", "New Name", "json"),
            ("short_name", "NEW", "NEW", "json"),
            ("country", "FR", "FR", "json"),
            ("founded_year", 1999, 1999, "json"),
            ("description", "Updated description", "Updated description", "json"),
            (
                "budget",
                "123456789.00",
                Decimal("123456789.00"),
                "json",
            ),  # Ожидаем родной Decimal
            ("budget_currency", "KZT", "KZT", "json"),
            ("main_sponsor", "New Sponsor", "New Sponsor", "json"),
            ("secondary_sponsor", "New Secondary", "New Secondary", "json"),
            ("logo", get_simple_upload_file(IMAGE_PATH), True, "multipart"),
            ("banner", get_simple_upload_file(IMAGE_PATH), True, "multipart"),
        ]

        for field, payload_value, expected_value, req_format in cases:
            with self.subTest(field=field):
                response = self.api_client.patch(
                    self.url,
                    {field: payload_value},
                    format=req_format,
                    HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
                )

                logger.debug("%s [%s]: %s", self._testMethodName, field, response.text)
                self.assertEqual(response.status_code, 200)

                self.team.refresh_from_db()
                actual_value = getattr(self.team, field)

                if field in ["logo", "banner"]:
                    self.assertTrue(bool(actual_value))
                else:
                    self.assertEqual(actual_value, expected_value)

    def test_full_update_success(self) -> None:
        data = {
            "name": "Full Updated Team",
            "short_name": "FUT",
            "country": "JP",
            "founded_year": 2020,
            "description": "Full update description",
            "budget": "777777.00",
            "budget_currency": "JPY",
            "main_sponsor": "Sony",
            "secondary_sponsor": "Toyota",
        }

        response = self.api_client.put(
            self.url,
            data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )

        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 200)

        self.team.refresh_from_db()
        self.assertEqual(self.team.name, data["name"])
        self.assertEqual(self.team.short_name, data["short_name"])
        self.assertEqual(str(self.team.country), data["country"])
        self.assertEqual(self.team.founded_year, data["founded_year"])
        self.assertEqual(self.team.description, data["description"])
        self.assertEqual(self.team.budget_currency, data["budget_currency"])
        self.assertEqual(self.team.main_sponsor, data["main_sponsor"])
        self.assertEqual(self.team.secondary_sponsor, data["secondary_sponsor"])

    def test_update_by_unauthorized_user_not_allowed(self) -> None:
        response = self.api_client.patch(self.url, {"name": "Hacked"})
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 401)

    def test_update_by_ordinary_user_not_allowed(self) -> None:
        response = self.api_client.patch(
            self.url, {"name": "Hacked"}, HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )
        logger.debug("%s: %s", self._testMethodName, response.text)
        self.assertEqual(response.status_code, 403)

    def test_update_with_invalid_budget_currency(self) -> None:
        for value in ["US", "USDX", "1"]:
            assert_validation_error(
                self=self,
                method="patch",
                url=self.url,
                data={"budget_currency": value},
                field="budget_currency",
                token=self.staff_token,
            )

    def test_update_with_invalid_country_code(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"country": "INVALID"},
            field="country",
            token=self.staff_token,
        )

    def test_update_with_duplicate_name_not_allowed(self) -> None:
        create_team(name="Existing Unique Team")

        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"name": "Existing Unique Team"},
            field="name",
            token=self.staff_token,
        )

    def test_update_with_duplicate_short_name_not_allowed(self) -> None:
        create_team(short_name="EXT")

        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"short_name": "EXT"},
            field="short_name",
            token=self.staff_token,
        )

    def test_update_name_exceeding_max_length(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"name": "A" * 256},
            field="name",
            token=self.staff_token,
        )

    def test_update_founded_year_exceeding_integer_limit(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"founded_year": 32768},
            field="founded_year",
            token=self.staff_token,
        )

    def test_update_budget_exceeding_max_digits(self) -> None:
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"budget": "10000000000000.00"},
            field="budget",
            token=self.staff_token,
        )

    def test_update_with_blank_strings_clears_optional_fields(self) -> None:
        data = {
            "description": "",
            "main_sponsor": "",
            "secondary_sponsor": "",
            "budget_currency": "",
        }
        response = self.api_client.patch(
            self.url,
            data,
            HTTP_AUTHORIZATION=f"Bearer {self.staff_token}",
        )
        self.assertEqual(response.status_code, 200)

        self.team.refresh_from_db()
        self.assertEqual(self.team.description, "")
        self.assertEqual(self.team.main_sponsor, "")
        self.assertEqual(self.team.secondary_sponsor, "")
        self.assertEqual(self.team.budget_currency, "")

    def test_update_invalid_logo_file_type(self) -> None:
        from django.core.files.uploadedfile import SimpleUploadedFile

        invalid_file = SimpleUploadedFile(
            "hacker.txt", b"not_a_valid_image_content", content_type="text/plain"
        )
        assert_validation_error(
            self=self,
            method="patch",
            url=self.url,
            data={"logo": invalid_file},
            field="logo",
            token=self.staff_token,
        )

    def test_put_update_missing_required_fields_fails(self) -> None:
        incomplete_data = {
            "short_name": "UPD",
            "country": "US",
        }
        assert_validation_error(
            self=self,
            method="put",
            url=self.url,
            data=incomplete_data,
            field="name",
            token=self.staff_token,
        )
