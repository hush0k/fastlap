from rest_framework.serializers import ModelSerializer

from apps.races.serializers import SeriesSerializer

from .models import Tournament


class TournamentListSerializer(ModelSerializer):
    series = SeriesSerializer()

    class Meta:
        model = Tournament
        fields = "__all__"


class TournamentCreateSerializer(ModelSerializer):
    class Meta:
        model = Tournament
        fields = (
            "name",
            "series",
            "description",
            "status",
            "is_active",
            "year",
            "start_date",
            "end_date",
            "total_rounds",
            "logo",
        )


class TournamentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Tournament
        fields = (
            "name",
            "series",
            "description",
            "status",
            "is_active",
            "year",
            "start_date",
            "end_date",
            "total_rounds",
            "logo",
        )
        extra_kwargs = {field: {"required": False} for field in fields}
