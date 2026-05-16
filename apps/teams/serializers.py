from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.teams.models import Team, TeamStandings


class TeamStandingsSerializer(serializers.ModelSerializer):
    tournament_name = serializers.CharField(source="tournament.name", read_only=True)
    tournament_slug = serializers.CharField(source="tournament.slug", read_only=True)

    class Meta:
        model = TeamStandings
        fields = [
            "id",
            "team",
            "tournament",
            "tournament_name",
            "tournament_slug",
            "points",
            "position",
        ]


class TeamListSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "short_name",
            "logo",
            "banner",
            "slug",
            "country",
            "country_name",
            "founded_year",
        ]


class TeamDetailSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source="country.name", read_only=True)
    standings = TeamStandingsSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "slug",
            "short_name",
            "logo",
            "banner",
            "country",
            "country_name",
            "founded_year",
            "description",
            "budget",
            "budget_currency",
            "main_sponsor",
            "secondary_sponsor",
            "standings",
            "created_at",
            "updated_at",
        ]


class TeamWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "name",
            "short_name",
            "logo",
            "banner",
            "country",
            "founded_year",
            "description",
            "budget",
            "budget_currency",
            "main_sponsor",
            "secondary_sponsor",
        ]

    def validate_budget_currency(self, value):
        if value and len(value) != 3:
            raise serializers.ValidationError(
                _(
                    "budget_currency must be a 3-letter currency code like USD, EUR, or KZT."  # noqa: E501
                )
            )
        return value.upper() if value else value
