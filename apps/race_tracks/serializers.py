from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.race_tracks.models import Track
from logging import getLogger

from config.settings.base import APP_LOGGER_NAME
from decimal import Decimal

logger = getLogger(APP_LOGGER_NAME)

class RaceTrackSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = Track
        fields = [
            "id",
            "name",
            "slug",
            "country_name",
            "city",
            "length_km",
            "number_of_turns",
        ]


class RaceTrackDetailSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source="country.name", read_only=True)
    country_code = serializers.CharField(source="country.code", read_only=True)

    class Meta:
        model = Track
<<<<<<< HEAD
        fields = [
            "id",
            "name",
            "slug",
            "country_name",
            "country_code",
            "city",
            "length_km",
            "lap_record",
            "number_of_turns",
            "map_image",
            "created_at",
            "updated_at",
        ]
=======
        fields = ['id', 'name', 'slug', 'country_name', 'country_code', 'city',
                 'length_km', 'lap_record', 'number_of_turns', 'map_image', 
                 'created_at', 'updated_at']
>>>>>>> 0e6107e1c089943cbfda7566fea209a804af52ae


class RaceTracksCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            "name",
            "country",
            "city",
            "length_km",
            "lap_record",
            "number_of_turns",
            "map_image",
        ]

    def validate_length_km(self, value: Decimal) -> Decimal:
        if value <= 0:
<<<<<<< HEAD
            raise serializers.ValidationError(_("Length km must be greater than 0"))
        return value
=======
            logger.info("Validation failed: length_km must be greater than 0")
            raise serializers.ValidationError('Length km must be greater than 0')
        return value
>>>>>>> 0e6107e1c089943cbfda7566fea209a804af52ae
