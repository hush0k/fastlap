from json import loads
from logging import getLogger

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.users.models import User
from tests.config import IMAGE_PATH, LARGE_AVATAR, TEST_LOGGER_NAME, firestore_service
from tests.utils import get_image_bytes, get_image_content_type

logger = getLogger(TEST_LOGGER_NAME)


class TestRegister(TestCase):
    register_url = reverse("register")

    def setUp(self) -> None:
        self.valid_data_with_avatar = {
            "email": "smile@example.com",
            "password": "MyPassword1234!",
            "username": "smile",
            "first_name": "smile",
            "last_name": "kun",
            "avatar": SimpleUploadedFile(
                name="avatar.png",
                content=get_image_bytes(IMAGE_PATH),
                content_type=get_image_content_type(IMAGE_PATH),
            ),
        }
        self.valid_data = {
            "email": "smile@example.com",
            "password": "MyPassword1234!",
            "username": "smile",
            "first_name": "smile",
            "last_name": "kun",
        }

    def test_success_register(self) -> None:
        response = self.client.post(self.register_url, self.valid_data_with_avatar)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email=self.valid_data["email"]).exists())

        user = User.objects.get(email=self.valid_data["email"])
        img_base64 = firestore_service.get_user_avatar(user.id)

        self.assertIsNotNone(img_base64)

    def test_success_without_avatar(self) -> None:
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email=self.valid_data["email"]).exists())

    def test_too_large_avatar(self) -> None:
        self.valid_data["avatar"] = SimpleUploadedFile(  # type: ignore
            name="avatar.png",
            content=get_image_bytes(LARGE_AVATAR),
            content_type=get_image_content_type(LARGE_AVATAR),
        )

        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Avatar size must be", loads(response.text)["avatar"][0])

    def test_email_or_username_already_exists(self) -> None:
        User.objects.create_user(**self.valid_data)
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(
            "User with this email already exists.", loads(response.text)["email"][0]
        )

        self.assertEqual(
            "User with this username already exists.",
            loads(response.text)["username"][0],
        )

    def test_bad_password_too_short(self) -> None:
        self.valid_data["password"] = "short"
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)

    def test_bad_password_without_special_symbols(self) -> None:
        self.valid_data["password"] = "WithoutSymbols1234"
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)

    def test_bad_password_only_lowercases(self) -> None:
        self.valid_data["password"] = "0nly_lowercases!"
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)

    def test_bad_password_no_digits(self) -> None:
        self.valid_data["password"] = "WithoutDigits!"
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self) -> None:
        self.valid_data["email"] = "invalid!email.com"
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            "Enter a valid email address.", loads(response.text)["email"][0]
        )

    def test_too_long_username(self) -> None:
        self.valid_data["username"] = "a" * 101
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)

    def test_too_long_first_name(self) -> None:
        self.valid_data["first_name"] = "a" * 101
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)

    def test_too_long_last_name(self) -> None:
        self.valid_data["last_name"] = "a" * 101
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)

    def test_too_long_password(self) -> None:
        self.valid_data["password"] = "A1!" + "a" * 126
        response = self.client.post(self.register_url, self.valid_data)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
