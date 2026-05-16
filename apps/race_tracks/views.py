"""
ViewSet for the race_tracks app.
"""

# Python modules

# Django modules
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

# Django REST Framework
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

# Project modules
from apps.common.services.redis_service import RedisService
from apps.drivers.permissions import IsStaffOrReadOnly
from apps.race_tracks.models import Track
from apps.race_tracks.serializers import (
    RaceTrackDetailSerializer,
    RaceTracksCreateSerializer,
    RaceTrackSerializer,
)


@extend_schema(tags=["Race Tracks"])
class RaceTrackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Race Track resources with Redis caching.
    """

    queryset = Track.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["country"]
    search_fields = ["name", "city"]
    ordering_fields = ["name", "length_km"]
    ordering = ["name"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return RaceTrackSerializer
        if self.action in ["create", "update", "partial_update"]:
            return RaceTracksCreateSerializer
        return RaceTrackDetailSerializer

    def _get_cache_key(self, request: Request, suffix: str = "") -> str:
        """Generate cache key for track requests."""
        key_parts = ["tracks"]

        query_params = request.GET.dict()
        if query_params:
            import hashlib
            import json

            params_hash = hashlib.md5(
                json.dumps(query_params, sort_keys=True).encode()
            ).hexdigest()[:8]
            key_parts.append(params_hash)

        offset = request.GET.get("offset", "0")
        limit = request.GET.get("limit", "20")
        key_parts.append(f"offset_{offset}")
        key_parts.append(f"limit_{limit}")

        if suffix:
            key_parts.append(suffix)

        return ":".join(key_parts)

    def _invalidate_track_cache(self):
        """Invalidate all track-related cache."""
        RedisService.delete_pattern("tracks:*")
        RedisService.delete_pattern("track:slug:*")

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle GET requests to list all tracks with caching (1 hour for static data).
        """
        cache_key = self._get_cache_key(request, "list")

        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response

        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            RedisService.set(cache_key, response, timeout=3600)

        return response

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle GET requests to retrieve a specific track with caching (1 hour).
        """
        slug = kwargs.get("slug", "")
        cache_key = f"track:slug:{slug}"

        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response

        response = super().retrieve(request, *args, **kwargs)

        if response.status_code == 200:
            RedisService.set(cache_key, response, timeout=3600)

        return response

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests to create a new track and invalidate cache.
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            self._invalidate_track_cache()
        return response

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle PUT/PATCH requests to update a track and invalidate cache.
        """
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            self._invalidate_track_cache()
        return response

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle DELETE requests to remove a track and invalidate cache.
        """
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            self._invalidate_track_cache()
        return response
