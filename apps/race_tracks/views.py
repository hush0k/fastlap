from rest_framework import serializers, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.race_tracks.models import Track
from apps.race_tracks.serializer import (
    RaceTrackSerializer,
    RaceTracksCreateSerializer,
    RaceTrackDetailSerializer,
)


class DjangoFilterBackend:
    pass


class RaceTrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.select_related("lap_record_holder").all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["country"]
    search_fields = ["name", "city"]
    ordering_fields = ["name", "length_km", "number_of_turns"]
    ordering = ["name"]

    def get_serializer_class(self) -> type[serializers.ModelSerializer]:
        if self.action == "list":
            return RaceTrackSerializer
        if self.action in ["create", "update", "partial_update"]:
            return RaceTracksCreateSerializer
        return RaceTrackDetailSerializer
