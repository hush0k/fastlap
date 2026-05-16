from logging import getLogger
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.core.validators import MaxLengthValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateField,
    DecimalField,
    ForeignKey,
    ImageField,
    PositiveSmallIntegerField,
    TextField,
    URLField,
)
from django.utils.translation import gettext as __
from django.utils.translation import gettext_lazy as _

from apps.common.enums import Currency, RaceStatusEnum
from apps.common.mixins import CreatedAtMixin, NameMixin, UpdatedAtMixin
from apps.common.models import BaseModel
from config.settings.base import (
    MEDIA_LOCATION,
    TOURNAMENT_LOGO_MAX_SIZE_BYTES,
    TOURNAMENT_LOGO_MAX_SIZE_MB,
)

logger = getLogger(__name__)


def logo_upload_path(instance: "Tournament", filename: str) -> str:
    """Return upload path for tournament logo using slug and original extension."""
    logger.debug(__("instance: %s, filename: %s"), instance.slug, filename)

    extension = Path(filename).suffix
    result = MEDIA_LOCATION.TOURNAMENTS_LOGO / str(instance.slug + extension)

    return str(result)


def validate_image_size(value: UploadedFile):
    """:raises raise ValidationError:"""
    logger.debug(__("image size: %s bytes"), value.size)

    if value.size > (TOURNAMENT_LOGO_MAX_SIZE_BYTES):
        raise ValidationError(
            __("Max image size is {0} MB").format(TOURNAMENT_LOGO_MAX_SIZE_MB)
        )


class Tournament(NameMixin, CreatedAtMixin, UpdatedAtMixin, BaseModel):
    series = ForeignKey(to="races.Series", on_delete=CASCADE)
    year = PositiveSmallIntegerField()
    status = CharField(
        max_length=10,
        choices=[(i.value, i.value) for i in RaceStatusEnum],
        default=RaceStatusEnum.FINISHED,
    )
    is_active = BooleanField(default=True)
    logo = ImageField(
        upload_to=logo_upload_path,
        validators=[validate_image_size],
        blank=True,
        null=True,
    )
    description = TextField(blank=True, validators=[MaxLengthValidator(7500)])
    start_date = DateField()
    end_date = DateField()
    total_rounds = PositiveSmallIntegerField()
    prize_fund = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = CharField(
        max_length=3,
        blank=True,
        choices=[(i.code, i.verbose) for i in Currency],
        default=Currency.USD,
    )
    regulations_url = URLField(blank=True)

    class Meta:
        ordering = ["start_date"]
        verbose_name = _("Tournament")
        verbose_name_plural = _("Tournaments")

    def __str__(self):
        return self.name


class TeamStanding(BaseModel):
    team = ForeignKey(to="teams.Team", on_delete=CASCADE)
    tournament = ForeignKey(to=Tournament, on_delete=CASCADE)
    position = PositiveSmallIntegerField()
    points = PositiveSmallIntegerField()


class DriverStanding(BaseModel):
    driver = ForeignKey(to="drivers.Driver", on_delete=CASCADE)
    tournament = ForeignKey(to=Tournament, on_delete=CASCADE)
    position = PositiveSmallIntegerField()
    points = PositiveSmallIntegerField()
