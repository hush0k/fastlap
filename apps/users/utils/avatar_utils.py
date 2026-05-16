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

        ext: str = Path(file.name).suffix.lower()
        if ext not in settings.ALLOWED_AVATAR_EXTENSIONS:
            return False, (
                f"File extension {ext} not allowed. "
                f"Allowed: {', '.join(settings.ALLOWED_AVATAR_EXTENSIONS)}"
            )

        try:
            file.seek(0)
            image: Image.Image = Image.open(file)
            image.verify()

            allowed_formats: list[str] = ["JPEG", "PNG", "GIF", "WEBP"]
            if image.format not in allowed_formats:
                return (
                    False,
                    f"Invalid image format. Supported: {', '.join(allowed_formats)}",
                )

            file.seek(0)


        except Exception as e:
            logger.error("Error validating image with Pillow: %s", e)
            return False, "Invalid image file - could not be opened as an image"


        return True, ""


    @staticmethod
    def resize_avatar(
        file: InMemoryUploadedFile,
        max_size: Tuple[int, int] = (300, 300),
    ) -> BytesIO:
        try:
            file.seek(0)
            image: Image.Image = Image.open(file)

            if image.mode in ("RGBA", "LA", "P"):
                rgb_image: Image.Image = Image.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(
                    image,
                    mask=image.split()[-1] if image.mode == "RGBA" else None,
                )
                image = rgb_image
            elif image.mode != "RGB":
                image = image.convert("RGB")
            elif image.mode != "RGB":
                image = image.convert("RGB")

            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            output: BytesIO = BytesIO()
            image.save(output, format="JPEG", quality=85, optimize=True)
            output.seek(0)


            return output

        except Exception as e:
            logger.error("Error resizing avatar: %s", e)
            raise


    @staticmethod
    def image_to_base64(image_bytes: BytesIO) -> str:
        image_base64: str = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{image_base64}"


    @staticmethod
    def process_avatar(
        file: InMemoryUploadedFile,
    ) -> Tuple[Optional[str], Optional[str]]:
        """Process avatar file and return (base64_string, error)."""
        is_valid, error = AvatarProcessor.validate_image(file)
        if not is_valid:
            return None, error


        try:
            resized_image: BytesIO = AvatarProcessor.resize_avatar(file)
            base64_string: str = AvatarProcessor.image_to_base64(resized_image)
            return base64_string, None

        except Exception as e:
            logger.error("Error processing avatar: %s", e)
            return None, "Error processing avatar image"
