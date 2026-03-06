from rest_framework import serializers

from apps.team_stuff.models import TeamStuff
from apps.teams.serializers import TeamListSerializer


class TeamStuffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamStuff
        fields = ("id", "fist_name", "last_name", "age", "country", "role")


class TeamStuffDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamStuff
        fields = (
            "id",
            "name",
            "slug",
            "fist_name",
            "last_name",
            "age",
            "country",
            "role",
            "description",
            "in_team_sincAe",
            "created_at",
            "updated_at",
        )


class TeamStuffCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamStuff
        fields = (
            "fist_name",
            "last_name",
            "age",
            "country",
            "role",
            "description",
            "in_team_sincAe",
        )


class TeamRosterDetailSerializer(serializers.Serializer):
    team = TeamListSerializer()
    stuff = TeamStuffListSerializer()

    class Meta:
        fields = (
            "team",
            "stuff",
            "start_date",
        )
