from pathlib import Path

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

from apps.common.enums import Currency, RaceStatusEnum
from apps.common.mixins import CreatedAtMixin, NameMixin, UpdatedAtMixin
from apps.common.models import BaseModel
from config.settings.base import MEDIA_LOCATION


def logo_upload_path(instance: "Tournament", filename: str) -> str:
    """Return upload path for tournament logo using slug and original extension."""

    extension = Path(filename).suffix
    result = MEDIA_LOCATION.TOURNAMENTS_LOGO / str(instance.slug + extension)

    return str(result)


class Tournament(NameMixin, CreatedAtMixin, UpdatedAtMixin, BaseModel):
    series = ForeignKey(to="races.Series", on_delete=CASCADE)
    year = PositiveSmallIntegerField()
    status = CharField(
        max_length=10,
        choices=[(i.value, i.value) for i in RaceStatusEnum],
        default=RaceStatusEnum.FINISHED,
    )
    is_active = BooleanField(default=True)
    logo = ImageField(upload_to=logo_upload_path, blank=True, null=True)
    description = TextField(blank=True)
    start_date = DateField()
    end_date = DateField()
    total_rounds = PositiveSmallIntegerField()
    prize_fund = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = CharField(
        max_length=3,
        blank=True,
        choices=[(i.code, i.verbose) for i in Currency],
        default=Currency.USD.code,
    )
    regulations_url = URLField(blank=True)

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"

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
