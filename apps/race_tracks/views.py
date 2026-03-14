from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import BaseSerializer

from apps.race_tracks.models import Track
from apps.race_tracks.serializer import (
    RaceTrackDetailSerializer,
    RaceTrackSerializer,
    RaceTracksCreateSerializer,
)


@extend_schema(tags=["Race Tracks"])
class RaceTrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.select_related("lap_record_holder").all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["name", "city"]
    ordering_fields = ["name", "length_km", "number_of_turns"]
    ordering = ["name"]

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action == "list":
            return RaceTrackSerializer
        if self.action in ["create", "update", "partial_update"]:
            return RaceTracksCreateSerializer
        return RaceTrackDetailSerializer