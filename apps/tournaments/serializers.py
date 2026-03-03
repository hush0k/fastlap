from rest_framework.serializers import ModelSerializer

from apps.races.serializers import SeriesSerializer

from .models import Tournament


class TournamentListSerializer(ModelSerializer):
    series = SeriesSerializer()

    class Meta:
        model = Tournament
        fields = "__all__"
