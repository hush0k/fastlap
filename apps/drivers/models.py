from django.db.models import (
    CharField,
    SlugField,
    DateField,
    PositiveIntegerField,
    ImageField,
    TextField,
    BooleanField,
    DecimalField,
    ForeignKey,
    PROTECT,
)
from django.utils.text import slugify
from django_countries.fields import CountryField
from pathlib import Path

from apps.common.models import BaseModel
from apps.common.mixins import CreatedAtMixin, UpdatedAtMixin
from apps.drivers.enums import DriverResultStatusEnum
from config.settings.base import MEDIA_LOCATION


def profile_image_upload_path(instance: "Driver", filename: str) -> str:
    extension = Path(filename).suffix
    result = MEDIA_LOCATION.DRIVER_PROFILE_IMAGE / str(instance.slug + extension)
    return str(result)


class Driver(CreatedAtMixin, UpdatedAtMixin, BaseModel):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    slug = SlugField(unique=True, blank=True)
    nationality = CountryField()
    date_of_birth = DateField(blank=True, null=True)
    number = PositiveIntegerField(blank=True, null=True)
    profile_image = ImageField(
        upload_to=profile_image_upload_path, blank=True, null=True
    )
    bio = TextField(blank=True, null=True)
    is_active = BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)


class DriverResult(CreatedAtMixin, UpdatedAtMixin, BaseModel):
    driver = ForeignKey(to=Driver, on_delete=PROTECT)
    race = ForeignKey(to="races.Race", on_delete=PROTECT)
    position = PositiveIntegerField(blank=True, null=True)
    grid_position = PositiveIntegerField(blank=True, null=True)
    points = DecimalField(max_digits=6, decimal_places=2)
    status = CharField(
        max_length=10, choices=[(i.value, i.value) for i in DriverResultStatusEnum]
    )
    fastest_lap = BooleanField(default=False)
    laps_completed = PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ("driver", "race")

    def __str__(self) -> str:
        return f"{self.driver} - {self.race} (P{self.position})"
