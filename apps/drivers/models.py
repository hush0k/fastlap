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
from django.utils.translation import gettext_lazy as _

from apps.common.mixins import CreatedAtMixin, UpdatedAtMixin
from apps.common.models import BaseModel
from apps.drivers.enums import DriverResultStatusEnum
from config.settings.base import MEDIA_LOCATION


def profile_image_upload_path(instance: "Driver", filename: str) -> str:
    extension = Path(filename).suffix
    result = MEDIA_LOCATION.DRIVER_PROFILE_IMAGE / str(instance.slug + extension)
    return str(result)


def driver_slug(instance):
    return f"{instance.first_name}-{instance.last_name}"


class Driver(CreatedAtMixin, UpdatedAtMixin, BaseModel):
    first_name = CharField(max_length=100, verbose_name=_("First Name"))
    last_name = CharField(max_length=100, verbose_name=_("Last Name"))
    slug = AutoSlugField(
        populate_from=driver_slug,
        unique=True,
    )  # type: ignore
    nationality = CountryField(verbose_name=_("Nationality"))
    date_of_birth = DateField(blank=True, null=True, verbose_name=_("Date of Birth"))
    number = PositiveIntegerField(blank=True, null=True, verbose_name=_("Racing Number"))  # noqa: E501
    profile_image = ImageField(
        upload_to=profile_image_upload_path,
        blank=True,
        null=True,
        verbose_name=_("Profile Image"),
    )
    bio = TextField(blank=True, null=True, verbose_name=_("Bio"))
    is_active = BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class DriverResult(CreatedAtMixin, UpdatedAtMixin, BaseModel):
    driver = ForeignKey(
        to=Driver,
        on_delete=PROTECT,
        related_name="results",
        verbose_name=_("Driver"),
    )
    race = ForeignKey(
        to="races.Race",
        on_delete=PROTECT,
        related_name="driver_results",
        verbose_name=_("Race"),
    )
    position = PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Finish Position")
    )
    grid_position = PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Grid Position")
    )
    points = DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Points"))
    status = CharField(
        max_length=10,
        choices=[(i.value, i.value) for i in DriverResultStatusEnum],
        verbose_name=_("Status"),
    )
    fastest_lap = BooleanField(default=False, verbose_name=_("Fastest Lap"))
    laps_completed = PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Laps Completed")
    )

    class Meta:
        verbose_name = _("Driver Result")
        verbose_name_plural = _("Driver Results")
        unique_together = ("driver", "race")

    def __str__(self) -> str:
        return f"{self.driver} - {self.race} (P{self.position})"
