from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.drivers.permissions import IsStaffOrReadOnly
from apps.teams.models import Team
from apps.teams.serializers import (
    TeamDetailSerializer,
    TeamListSerializer,
    TeamStandingsSerializer,
    TeamWriteSerializer,
)


@extend_schema(tags=["Teams"])
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().prefetch_related("standings__tournament")
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["name", "founded_year"]
    ordering = ["name"]
    search_fields = ["name", "short_name", "country"]
    filterset_fields = ["country", "founded_year"]

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action == "list":
            return TeamListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return TeamWriteSerializer
        return TeamDetailSerializer

    @action(methods=["get"], detail=True, url_path="standings")
    def standings(self, request: Request, slug: str | None = None) -> Response:
        team = self.get_object()
        standings = team.standings.select_related("tournament").all()
        serializer = TeamStandingsSerializer(standings, many=True)
        return Response(serializer.data)
