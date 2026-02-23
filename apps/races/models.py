from django.db.models import CharField, ImageField, TextField
from apps.common.models import BaseModel
from apps.common.mixins import CreatedAtMixin, UpdatedAtMixin, NameMixin
from apps.common.enums import SeriesCategoryEnum
from pathlib import Path
from config.settings.base import MEDIA_LOCATION


def logo_upload_path(instance: "Series", filename: str) -> str:
    """Return upload path for series logo using slug and original extension."""

    extension = Path(filename).suffix
    result = MEDIA_LOCATION.SERIES_LOGO / str(instance.slug + extension)

    return str(result)


class Series(NameMixin, BaseModel):
    category = CharField(
        max_length=10, choices=[(i.value, i.value) for i in SeriesCategoryEnum]
    )
    description = TextField(blank=True, null=True)
    logo = ImageField(upload_to=logo_upload_path, blank=True, null=True)


class Races(NameMixin, CreatedAtMixin, UpdatedAtMixin, BaseModel):
    pass
