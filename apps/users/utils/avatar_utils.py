import base64
import logging
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class AvatarProcessor:
    @staticmethod
    def validate_image(file: InMemoryUploadedFile) -> Tuple[bool, str]:
        if file.size > settings.AVATAR_MAX_SIZE_BYTES:
            return (
                False,
                _(f"Avatar size must be <= {settings.AVATAR_MAX_SIZE_MB}MB"),
            )

        ext = Path(file.name).suffix.lower()
        if ext not in settings.ALLOWED_AVATAR_EXTENSIONS:
            return (
                False,
                _(
                    f"File extension {ext} not allowed. Allowed: {', '.join(settings.ALLOWED_AVATAR_EXTENSIONS)}"  # noqa: E501
                ),
            )

        try:
            file.seek(0)

            image = Image.open(file)
            image.verify()

            allowed_formats = ["JPEG", "PNG", "GIF", "WEBP"]
            if image.format not in allowed_formats:
                return (
                    False,
                    _(f"Invalid image format. Supported: {', '.join(allowed_formats)}"),
                )

            file.seek(0)

        except Exception as e:
            logger.error(_(f"Error validating image with Pillow: {e}"))
            return (
                False,
                _("Invalid image file - could not be opened as an image"),
            )

        return True, ""

    @staticmethod
    def resize_avatar(
        file: InMemoryUploadedFile, max_size: Tuple[int, int] = (300, 300)
    ) -> BytesIO:
        try:
            file.seek(0)

            image = Image.open(file)

            if image.mode in ("RGBA", "LA", "P"):
                rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(
                    image, mask=image.split()[-1] if image.mode == "RGBA" else None
                )
                image = rgb_image
            elif image.mode != "RGB":
                image = image.convert("RGB")

            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            output = BytesIO()
            image.save(output, format="JPEG", quality=85, optimize=True)
            output.seek(0)

            return output
        except Exception as e:
            logger.error(_(f"Error resizing avatar: {e}"))
            raise

    @staticmethod
    def image_to_base64(image_bytes: BytesIO) -> str:
        image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{image_base64}"

    @staticmethod
    def process_avatar(
        file: InMemoryUploadedFile,
    ) -> Tuple[Optional[str], Optional[str]]:
        """Process avatar file and return base64 string"""
        is_valid, error = AvatarProcessor.validate_image(file)
        if not is_valid:
            return None, error

        try:
            resized_image = AvatarProcessor.resize_avatar(file)

            base64_string = AvatarProcessor.image_to_base64(resized_image)

            return base64_string, None
        except Exception as e:
            logger.error(_(f"Error processing avatar: {e}"))
            return (
                None,
                _("Error processing avatar image"),
            )
