from logging import getLogger
from pathlib import Path
from typing import Literal

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.users.models import User
from tests.config import TEST_LOGGER_NAME

HTTPMethod = Literal["post", "patch", "put"]

logger = getLogger(TEST_LOGGER_NAME)


def get_image_bytes(file: str | Path) -> bytes:
    with open(file, mode="rb") as f:
        result = f.read()
    return result


def get_image_content_type(file: str | Path) -> str:
    image = Image.open(file)
    return Image.MIME[image.format]


def get_simple_upload_file(file_path: Path, empty: bool = False) -> SimpleUploadedFile:
    if empty:
        content = "".encode()
    else:
        content = get_image_bytes(file_path)

    return SimpleUploadedFile(
        name=file_path.name,
        content=content,
        content_type=get_image_content_type(file_path),
    )


def get_user(*_, **kwargs) -> User:
    user_data = dict(
        email="smile@example.com",
        username="smile",
        first_name="smile",
        last_name="kun",
        password="MyPassword1234!",
    )
    user_data.update(**kwargs)
    user = User.objects.create_user(**user_data)
    return user


def assert_validation_error(
    *,
    self,
    method: HTTPMethod,
    url: str,
    data: dict,
    field: str,
    token: str | None,
    expected_status: int = 400,
) -> None:
    request_method = getattr(self.api_client, method)

    headers = {}

    if token:
        headers["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    response = request_method(
        url,
        data,
        **headers,
    )

    logger.debug(
        "%s [%s] %s: %s",
        self._testMethodName,
        method.upper(),
        data,
        response.text,
    )

    self.assertEqual(response.status_code, expected_status)
    self.assertIn(field, response.json())
