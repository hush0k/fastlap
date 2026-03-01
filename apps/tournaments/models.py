from django.db.models import (
    CharField,
    DateField,
    DecimalField,
    TextField,
)

from apps.common.enums import Currency
from apps.common.mixins import CreatedAtMixin, NameMixin, UpdatedAtMixin
from apps.common.models import BaseModel


class Tournament(NameMixin, CreatedAtMixin, UpdatedAtMixin, BaseModel):
    description = TextField(blank=True)
    start_date = DateField()
    end_date = DateField()
    location = CharField(max_length=255, blank=True)
    prize_pool = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = CharField(
        max_length=3,
        blank=True,
        choices=[(i.code, i.verbose) for i in Currency],
        default=Currency.USD.code,
    )
    organizer = CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"

    def __str__(self):
        return self.name
