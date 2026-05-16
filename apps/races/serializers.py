"""
Serializers for the races app.
"""

# Python modules

# Django REST Framework
from rest_framework import serializers

# Project modules
from apps.races.models import Race, Series


class SeriesListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Series.
    """

    class Meta:
        model = Series
        fields = ["id", "name", "slug", "category", "logo", "created_at"]


class SeriesDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Series view.
    """

    class Meta:
        model = Series
        fields = "__all__"


class SeriesWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating Series.
    """

    class Meta:
        model = Series
        fields = ["name", "category", "description", "logo"]

    def validate_name(self, value: str) -> str:
        """
        Validate series name is not empty.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Series name cannot be empty.")
        return value.strip()


class RaceListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Races.
    """

    series_name = serializers.CharField(source="series.name", read_only=True)
    series_slug = serializers.CharField(source="series.slug", read_only=True)

    class Meta:
        model = Race
        fields = [
            "id",
            "name",
            "slug",
            "series",
            "series_name",
            "series_slug",
            "round_number",
            "scheduled_at",
            "status",
            "watch_platform",
        ]


class RaceDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Race view.
    """

    series_name = serializers.CharField(source="series.name", read_only=True)
    series_slug = serializers.CharField(source="series.slug", read_only=True)
    series_category = serializers.CharField(source="series.category", read_only=True)

    class Meta:
        model = Race
        fields = "__all__"


class RaceWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating Races.
    """

    class Meta:
        model = Race
        fields = [
            "name",
            "series",
            "round_number",
            "scheduled_at",
            "status",
            "watch_url",
            "watch_platform",
            "laps_total",
        ]

    def validate_round_number(self, value: int) -> int:
        """
        Validate round number is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Round number must be greater than 0.")
        return value

    def validate_name(self, value: str) -> str:
        """
        Validate race name is not empty.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Race name cannot be empty.")
        return value.strip()

    def validate_laps_total(self, value: int) -> int:
        """
        Validate laps total is positive if provided.
        """
        if value is not None and value <= 0:
            raise serializers.ValidationError("Total laps must be greater than 0.")
        return value
