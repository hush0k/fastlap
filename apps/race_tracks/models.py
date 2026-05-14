from django.db import models
from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from apps.common.mixins import CreatedAtMixin, UpdatedAtMixin, NameMixin
from apps.common.models import BaseModel
from apps.drivers.models import Driver


class Track(CreatedAtMixin, UpdatedAtMixin, NameMixin, models.Model):
    country = CountryField()
    city = models.CharField(max_length=100)
    timezone = TimeZoneField(default="UTC")
    length_km = models.DecimalField(max_digits=10, decimal_places=2)
    lap_record = models.DurationField(null=True, blank=True)
    lap_record_holder = models.ForeignKey(
        Driver, on_delete=models.SET_NULL, null=True, related_name="track_record"
    )
    number_of_turns = models.PositiveIntegerField(default=0)
    map_image = models.ImageField(upload_to="tracks/maps/", null=True, blank=True)

    class Meta:
        ordering = ["name", "country"]

    def __str__(self):
        return f"{self.name} - {self.country}"