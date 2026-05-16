from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from django.db import models

from apps.common.mixins import CreatedAtMixin, NameMixin, UpdatedAtMixin
from apps.common.utils import get_image_size_validator
from apps.drivers.models import Driver
from config.settings.base import MAP_IMAGE_MAX_SIZE_BYTES

track_map_image_validator = get_image_size_validator(MAP_IMAGE_MAX_SIZE_BYTES)


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
    map_image = models.ImageField(
        upload_to="tracks/maps/",
        null=True,
        blank=True,
        validators=[track_map_image_validator],
    )

    class Meta:
        ordering = ["name", "country"]

    def __str__(self) -> str:
        return f"{self.name} - {self.country}"
