from rest_framework import serializers

from apps.teams.models import Team, TeamStandings


class TeamStandingsSerializer(serializers.ModelSerializer):
    tournament_name = serializers.CharField(source="tournament.name", read_only=True)

    class Meta:
        model = TeamStandings
        fields = [
            "team",
            "tournament",
            "tournament_name",
            "points",
            "position",
            "wins",
            "podiums",
            "def_count",
        ]


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "short_name", "logo", "slug", "country"]


class TeamDetailSerializer(serializers.ModelSerializer):
    standings = TeamStandingsSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "slug",
            "short_name",
            "logo",
            "country",
            "founded_year",
            "description",
            "budget",
            "budget_currency",
            "main_sponsor",
            "secondary_sponsor",
            "standings",
            "created_at",
            "updated_at",
            "standings",
        ]


class TeamWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "name",
            "short_name",
            "logo",
            "country",
            "founded_year",
            "description",
            "budget",
            "budget_currency",
            "main_sponsor",
            "secondary_sponsor",
        ]
