from drf_spectacular.contrib.django_filters import DjangoFilterExtension
from rest_framework import viewsets, filters
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.team_stuff.serializers import TeamStuffListSerializer, TeamStuffCreateSerializer, TeamStuffDetailSerializer


class TeamStuffViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    filter_backends = (OrderingFilter,SearchFilter, DjangoFilterExtension)
    ordering_fields = "country, role, id, in_team_sincAe"
    search_fields = "first_name, role, country"
    filterset_fields = "country, role"

    def get_serializer_class(self):
        if self.action == "list":
            return TeamStuffListSerializer
        elif self.action == ["create", "retrieve", "delete"]:
            return TeamStuffCreateSerializer
        return TeamStuffDetailSerializer





