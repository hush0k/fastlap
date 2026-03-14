from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.team_stuff.models import StaffMember
from apps.team_stuff.serializers import (
    StaffMemberDetailSerializer,
    StaffMemberListSerializer,
    StaffMemberWriteSerializer,
    TeamRosterSerializer,
)


class StaffMemberViewSet(viewsets.ModelViewSet):
    queryset = StaffMember.objects.prefetch_related("rosters__team").all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["country", "role"]
    search_fields = ["first_name", "last_name", "role"]
    ordering_fields = ["last_name", "role", "country"]
    ordering = ["last_name"]

    def get_serializer_class(self):
        if self.action == "list":
            return StaffMemberListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return StaffMemberWriteSerializer
        return StaffMemberDetailSerializer

    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request, slug=None):
        """История команд сотрудника"""
        member = self.get_object()
        rosters = member.rosters.select_related("team").order_by("-start_date")
        serializer = TeamRosterSerializer(rosters, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="current-team")
    def current_team(self, request, slug=None):
        """Текущая активная команда"""
        member = self.get_object()
        roster = member.rosters.filter(is_active=True).select_related("team").first()
        if not roster:
            return Response({"detail": "Не состоит ни в одной команде."}, status=404)
        serializer = TeamRosterSerializer(roster)
        return Response(serializer.data)
