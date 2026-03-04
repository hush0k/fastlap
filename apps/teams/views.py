from drf_spectacular.contrib.django_filters import DjangoFilterExtension

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.teams.models import Team
from apps.teams.serializers import (
    TeamDetailSerializer,
    TeamListSerializer,
    TeamStandingsSerializer,
    TeamWriteSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().prefetch_related("standings__tournament")
    lookup_field = "slug"
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterExtension)
    ordering_fields = "standings__position", "name", "founded_year"
    search_fields = "name", "short_name", "country"
    filterset_fields = "country", "founded_year"

    def get_serializer_class(self):
        if self.action == "list":
            return TeamListSerializer
        elif self.action == ["create", "update", "partial_update"]:
            return TeamWriteSerializer
        return TeamDetailSerializer

    @action(methods=["get"], detail=True, url_path="standings")
    def standings(self, request, slug=None):
        team = self.get_object()
        standings = team.standings.filter(team=team).select_related("tournament")
        serializer = TeamStandingsSerializer(standings, many=True)
        return Response(serializer.data)
