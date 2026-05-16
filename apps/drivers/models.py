from logging import getLogger
from pathlib import Path

from autoslug import AutoSlugField
from django_countries.fields import CountryField

from django.core.files.uploadedfile import UploadedFile
from django.core.validators import MaxLengthValidator
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
from rest_framework.exceptions import ValidationError

from apps.common.mixins import CreatedAtMixin, UpdatedAtMixin
from apps.common.models import BaseModel
from apps.drivers.enums import DriverResultStatusEnum
from config.settings.base import (
    APP_LOGGER_NAME,
    DRIVER_IMAGE_MAX_SIZE_BYTES,
    DRIVER_IMAGE_MAX_SIZE_MB,
    MEDIA_LOCATION,
)

logger = getLogger(APP_LOGGER_NAME)


def profile_image_upload_path(instance: "Driver", filename: str) -> str:
    extension: str = Path(filename).suffix
    result: Path = MEDIA_LOCATION.DRIVER_PROFILE_IMAGE / str(instance.slug + extension)
    return str(result)


def driver_slug(instance: "Driver") -> str:
    return f"{instance.first_name}-{instance.last_name}"


def validate_profile_image_size(value: UploadedFile) -> None:
    """:raises ValidationError: if file exceeds the max allowed size."""
    logger.debug("image size: %s", value.size)
    if value.size > DRIVER_IMAGE_MAX_SIZE_BYTES:
        raise ValidationError(f"Max image size is {DRIVER_IMAGE_MAX_SIZE_MB} MB")


class Driver(CreatedAtMixin, UpdatedAtMixin, BaseModel):
    first_name = CharField(max_length=100, verbose_name=_("First Name"))
    last_name = CharField(max_length=100, verbose_name=_("Last Name"))
    slug = AutoSlugField(
        populate_from=driver_slug,
        unique=True,
    )  # type: ignore
    nationality = CountryField(verbose_name=_("Nationality"))
    date_of_birth = DateField(blank=True, null=True, verbose_name=_("Date of Birth"))
    number = PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Racing Number")
    )  # noqa: E501
    profile_image = ImageField(
        validators=[validate_profile_image_size],
        upload_to=profile_image_upload_path,
        blank=True,
        null=True,
        verbose_name=_("Profile Image"),
    )
    bio: TextField = TextField(
        blank=True,
        null=True,
        verbose_name=_("Bio"),
        validators=[MaxLengthValidator(15_000)],
    )
    is_active: BooleanField = BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class DriverResult(CreatedAtMixin, UpdatedAtMixin, BaseModel):
    driver: ForeignKey = ForeignKey(
        to=Driver,
        on_delete=PROTECT,
        related_name="results",
        verbose_name=_("Driver"),
    )
    race: ForeignKey = ForeignKey(
        to="races.Race",
        on_delete=PROTECT,
        related_name="driver_results",
        verbose_name=_("Race"),
    )
    position: PositiveIntegerField = PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Finish Position")
    )
    grid_position: PositiveIntegerField = PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Grid Position")
    )
    points: DecimalField = DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Points")
    )
    status: CharField = CharField(
        max_length=10,
        choices=[(i.value, i.value) for i in DriverResultStatusEnum],
        verbose_name=_("Status"),
    )
    fastest_lap: BooleanField = BooleanField(
        default=False, verbose_name=_("Fastest Lap")
    )
    laps_completed: PositiveIntegerField = PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Laps Completed")
    )

    class Meta:
        verbose_name = _("Driver Result")
        verbose_name_plural = _("Driver Results")
        unique_together = ("driver", "race")

    def __str__(self) -> str:
        return f"{self.driver} - {self.race} (P{self.position})"
