from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from apps.drivers.permissions import IsStaffOrReadOnly
from apps.race_tracks.models import Track
from apps.race_tracks.schema.custom_schema import RaceTrackAutoSchema
from apps.race_tracks.serializers import (
    RaceTrackSerializer,
    RaceTracksCreateSerializer,
    RaceTrackDetailSerializer
)


class RaceTrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country']
    search_fields = ['name', 'city']
    ordering_fields = ['name', 'length_km']
    ordering = ['name']
    lookup_field = 'slug'
    schema = RaceTrackAutoSchema()

    def get_serializer_class(self):
        if self.action == 'list':
            return RaceTrackSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return RaceTracksCreateSerializer
        return RaceTrackDetailSerializer