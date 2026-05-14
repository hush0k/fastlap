from pathlib import Path

from PIL import Image


def get_image_bytes(file: str | Path) -> bytes:
    with open(file, mode="rb") as f:
        result = f.read()
    return result


def get_image_content_type(file: str | Path) -> str:
    image = Image.open(file)
    return Image.MIME[image.format]
