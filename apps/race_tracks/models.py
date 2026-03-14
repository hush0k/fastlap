from django.db import models
from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from apps.common.mixins import CreatedAtMixin, UpdatedAtMixin, NameMixin
from apps.common.models import BaseModel
from apps.drivers.models import Driver


class Track(CreatedAtMixin, UpdatedAtMixin, NameMixin, models.Model):
    country: CountryField = CountryField()
    city: models.CharField = models.CharField(max_length=100)
    timezone: TimeZoneField = TimeZoneField(default="UTC")
    length_km: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    lap_record: models.DurationField = models.DurationField(null=True, blank=True)
    lap_record_holder: models.ForeignKey = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        related_name="track_record",
    )
    number_of_turns: models.PositiveIntegerField = models.PositiveIntegerField(default=0)
    map_image: models.ImageField = models.ImageField(
        upload_to="tracks/maps/", null=True, blank=True
    )

    class Meta:
        ordering = ["name", "country"]

    def __str__(self) -> str:
        return f"{self.name} - {self.country}"