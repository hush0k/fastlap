from typing import Optional

from rest_framework import serializers
from apps.team_stuff.models import StaffMember, TeamRoster


class TeamRosterSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source="team.name", read_only=True)
    team_short = serializers.CharField(source="team.short_name", read_only=True)

    class Meta:
        model = TeamRoster
        fields = [
            "id",
            "team_name",
            "team_short",
            "start_date",
            "end_date",
            "is_active",
        ]


class StaffMemberListSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="country.name")
    current_team = serializers.SerializerMethodField()

    class Meta:
        model = StaffMember
        fields = ["id", "full_name", "role", "country", "photo", "current_team"]

    def get_current_team(self, obj: StaffMember) -> Optional[str]:
        roster = obj.rosters.filter(is_active=True).select_related("team").first()
        if roster:
            return roster.team.short_name
        return None


class StaffMemberDetailSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="country.name")
    country_code = serializers.CharField(source="country.code")
    rosters = TeamRosterSerializer(many=True, read_only=True)

    class Meta:
        model = StaffMember
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "age",
            "country",
            "country_code",
            "role",
            "description",
            "photo",
            "rosters",
            "created_at",
            "updated_at",
        ]


class StaffMemberWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = [
            "first_name",
            "last_name",
            "age",
            "country",
            "role",
            "description",
            "photo",
        ]

    def validate_age(self, value: Optional[int]) -> Optional[int]:
        if value is not None and not (16 <= value <= 80):
            raise serializers.ValidationError("Возраст должен быть от 16 до 80.")
        return value
