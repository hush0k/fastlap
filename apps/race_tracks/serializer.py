from rest_framework import serializers

from apps.drivers.serializers import DriverDetailSerializer
from apps.race_tracks.models import Track


class RaceTrackSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="country.name")

    class Meta:
        model = Track
        fields = ["id", "name", "slug", "country", "city", "timezone", "length_km", "lap_record"]


class RaceTrackDetailSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="country.name")
    country_code = serializers.CharField(source="country.code")
    lap_record_hodlers = DriverDetailSerializer(read_only=True)

    class Meta:
        model = Track
        fields = "__all__"


class RaceTracksCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            "name",
            "country",
            "city",
            "timezone",
            "length_km",
            "lap_record",
            "lap_record_holder",
            "number_of_turns",
            "map_image"
        ]

    def validate_length_km(self, value):
        if value <= 0:
            raise serializers.ValidationError("Length km must be greater than 0")
        return value
