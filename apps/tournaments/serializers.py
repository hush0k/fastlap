"""
Serializers for the tournaments app.
"""

# Django REST Framework
from rest_framework import serializers

# Project modules
from apps.races.serializers import SeriesListSerializer
from apps.tournaments.models import Tournament


class TournamentListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Tournaments.
    """
    
    series = SeriesListSerializer()
    
    class Meta:
        model = Tournament
        fields = [
            "id",
            "name",
            "slug",
            "series",
            "year",
            "status",
            "is_active",
            "logo",
            "start_date",
            "end_date",
            "total_rounds",
            "prize_fund",
            "currency",
        ]


class TournamentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Tournament view.
    """
    
    series = SeriesListSerializer()
    
    class Meta:
        model = Tournament
        fields = [
            "id",
            "name",
            "slug",
            "series",
            "year",
            "status",
            "is_active",
            "logo",
            "description",
            "start_date",
            "end_date",
            "total_rounds",
            "prize_fund",
            "currency",
            "regulations_url",
            "created_at",
            "updated_at",
        ]


class TournamentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Tournaments.
    """
    
    class Meta:
        model = Tournament
        fields = [
            "name",
            "series",
            "description",
            "status",
            "is_active",
            "year",
            "start_date",
            "end_date",
            "total_rounds",
            "prize_fund",
            "logo",
            "regulations_url",
            "currency",
        ]


class TournamentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Tournaments.
    """
    
    class Meta:
        model = Tournament
        fields = [
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
        ]
        extra_kwargs = {field: {"required": False} for field in fields}