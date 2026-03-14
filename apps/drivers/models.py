from pathlib import Path

from autoslug import AutoSlugField
from django_countries.fields import CountryField

from django.db.models import (
    PROTECT,
    BooleanField,
    CharField,
    DateField,
    DecimalField,
    ForeignKey,
    ImageField,
    PositiveIntegerField,
    TextField,
)

from apps.common.mixins import CreatedAtMixin, UpdatedAtMixin
from apps.common.models import BaseModel
from apps.drivers.enums import DriverResultStatusEnum
from config.settings.base import MEDIA_LOCATION


def profile_image_upload_path(instance: "Driver", filename: str) -> str:
    extension: str = Path(filename).suffix
    result: Path = MEDIA_LOCATION.DRIVER_PROFILE_IMAGE / str(instance.slug + extension)
    return str(result)


def driver_slug(instance: "Driver") -> str:
    return f"{instance.first_name}-{instance.last_name}"


class Driver(CreatedAtMixin, UpdatedAtMixin, BaseModel):
    first_name: CharField = CharField(max_length=100, verbose_name="First Name")
    last_name: CharField = CharField(max_length=100, verbose_name="Last Name")
    slug: AutoSlugField = AutoSlugField(populate_from=driver_slug, unique=True)  # type: ignore[assignment]
    nationality: CountryField = CountryField(verbose_name="Nationality")
    date_of_birth: DateField = DateField(blank=True, null=True, verbose_name="Date of Birth")
    number: PositiveIntegerField = PositiveIntegerField(blank=True, null=True, verbose_name="Racing Number")
    profile_image: ImageField = ImageField(
        upload_to=profile_image_upload_path,
        blank=True,
        null=True,
        verbose_name="Profile Image",
    )
    bio: TextField = TextField(blank=True, null=True, verbose_name="Bio")
    is_active: BooleanField = BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class DriverResult(CreatedAtMixin, UpdatedAtMixin, BaseModel):
    driver: ForeignKey = ForeignKey(
        to=Driver,
        on_delete=PROTECT,
        related_name="results",
        verbose_name="Driver",
    )
    race: ForeignKey = ForeignKey(
        to="races.Race",
        on_delete=PROTECT,
        related_name="driver_results",
        verbose_name="Race",
    )
    position: PositiveIntegerField = PositiveIntegerField(
        blank=True, null=True, verbose_name="Finish Position"
    )
    grid_position: PositiveIntegerField = PositiveIntegerField(
        blank=True, null=True, verbose_name="Grid Position"
    )
    points: DecimalField = DecimalField(max_digits=6, decimal_places=2, verbose_name="Points")
    status: CharField = CharField(
        max_length=10,
        choices=[(i.value, i.value) for i in DriverResultStatusEnum],
        verbose_name="Status",
    )
    fastest_lap: BooleanField = BooleanField(default=False, verbose_name="Fastest Lap")
    laps_completed: PositiveIntegerField = PositiveIntegerField(
        blank=True, null=True, verbose_name="Laps Completed"
    )

    class Meta:
        verbose_name = "Driver Result"
        verbose_name_plural = "Driver Results"
        unique_together = ("driver", "race")

    def __str__(self) -> str:
        return f"{self.driver} - {self.race} (P{self.position})"