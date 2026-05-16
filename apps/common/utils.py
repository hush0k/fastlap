from typing import Callable

from django.core.files.uploadedfile import UploadedFile
from logging import getLogger

from django.core.exceptions import ValidationError

from config.settings.base import APP_LOGGER_NAME

logger = getLogger(APP_LOGGER_NAME)

def get_image_size_validator(image_size_in_bytes: int) -> Callable[[UploadedFile], None]:

    def validate_image_size(value: UploadedFile) -> None:
        """:raises ValidationError: if file exceeds the max allowed size."""
        logger.debug("image size: %s", value.size)
        if value.size > image_size_in_bytes:
            raise ValidationError(f"Max image size is {image_size_in_bytes / (1024 * 1024)} MB")

    return validate_image_size