from pathlib import Path

from django.db.models import (
    PROTECT,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    PositiveIntegerField,
    TextField,
    URLField,
)

from apps.common.enums import RaceStatusEnum, SeriesCategoryEnum, WatchPlatformEnum
from apps.common.mixins import CreatedAtMixin, NameMixin, UpdatedAtMixin
from apps.common.models import BaseModel
from config.settings.base import MEDIA_LOCATION


def logo_upload_path(instance: "Series", filename: str) -> str:
    """Return upload path for series logo using slug and original extension."""
    extension: str = Path(filename).suffix
    result: Path = MEDIA_LOCATION.SERIES_LOGO / str(instance.slug + extension)
    return str(result)


class Series(NameMixin, CreatedAtMixin, UpdatedAtMixin, BaseModel):
    category: CharField = CharField(
        max_length=10,
        choices=[(i.value, i.value) for i in SeriesCategoryEnum],
    )
    description: TextField = TextField(blank=True, null=True)
    logo: ImageField = ImageField(upload_to=logo_upload_path, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Race(NameMixin, CreatedAtMixin, UpdatedAtMixin, BaseModel):
    series: ForeignKey = ForeignKey(to=Series, on_delete=PROTECT)
    round_number: PositiveIntegerField = PositiveIntegerField()
    scheduled_at: DateTimeField = DateTimeField()
    status: CharField = CharField(
        max_length=10,
        choices=[(i.value, i.value) for i in RaceStatusEnum],
    )
    watch_url: URLField = URLField(max_length=255, blank=True, null=True)
    watch_platform: CharField = CharField(
        max_length=20,
        choices=[(i.value, i.value) for i in WatchPlatformEnum],
    )
    laps_total: PositiveIntegerField = PositiveIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name