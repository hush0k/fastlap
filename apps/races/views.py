"""
ViewSet for the races app.
"""

# Python modules
from typing import Any

# Django modules
from asgiref.sync import async_to_sync
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema

# Django REST Framework
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request as DRFRequest

# Project modules
from apps.common.pagination import CustomPagination
from apps.common.services.redis_service import RedisService
from apps.drivers.permissions import IsStaffOrReadOnly
from apps.races.models import Race, Series
from apps.races.serializers import (
    RaceDetailSerializer,
    RaceListSerializer,
    RaceWriteSerializer,
    SeriesDetailSerializer,
    SeriesListSerializer,
    SeriesWriteSerializer,
)


@extend_schema(tags=["Races"])
class SeriesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Series resources with Redis caching.

    Provides CRUD operations for racing series (Formula 1, MotoGP, etc.)
    """

    queryset = Series.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "category", "created_at"]
    ordering = ["name"]
    lookup_field = "slug"

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == "list":
            return SeriesListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return SeriesWriteSerializer
        return SeriesDetailSerializer

    def _invalidate_series_cache(self):
        """Invalidate all series-related cache."""
        async_to_sync(RedisService.delete_pattern)("series:*")
        async_to_sync(RedisService.delete_pattern)("series:slug:*")

    @extend_schema(
        summary="List Series",
        description="Retrieve a paginated list of all racing series.",
        responses={
            200: OpenApiResponse(
                description="Successful response with paginated series list.",
                response=SeriesListSerializer,
            ),
        },
    )
    def list(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle GET requests to list all series with caching.
        """
        cache_key = "series:list"

        cached_response = async_to_sync(RedisService.get)(cache_key)
        if cached_response:
            return cached_response

        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            async_to_sync(RedisService.set)(cache_key, response, timeout=3600)

        return response

    @extend_schema(
        summary="Create Series",
        description="Create a new racing series.",
        request=SeriesWriteSerializer,
        responses={
            201: OpenApiResponse(
                description="Series created successfully.",
                response=SeriesDetailSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid input data.",
            ),
        },
    )
    def create(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle POST requests to create a new series and invalidate cache.
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            self._invalidate_series_cache()
        return response

    @extend_schema(
        summary="Retrieve Series",
        description="Retrieve a specific racing series by slug.",
        responses={
            200: OpenApiResponse(
                description="Successful response with series details.",
                response=SeriesDetailSerializer,
            ),
            404: OpenApiResponse(
                description="Series not found.",
            ),
        },
    )
    def retrieve(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle GET requests to retrieve a specific series with caching.
        """
        slug = kwargs.get("slug", "")
        cache_key = f"series:slug:{slug}"

        cached_response = async_to_sync(RedisService.get)(cache_key)
        if cached_response:
            return cached_response

        response = super().retrieve(request, *args, **kwargs)

        if response.status_code == 200:
            async_to_sync(RedisService.set)(cache_key, response, timeout=3600)

        return response

    @extend_schema(
        summary="Update Series",
        description="Update an existing racing series.",
        request=SeriesWriteSerializer,
        responses={
            200: OpenApiResponse(
                description="Series updated successfully.",
                response=SeriesDetailSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid input data.",
            ),
            404: OpenApiResponse(
                description="Series not found.",
            ),
        },
    )
    def update(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle PUT/PATCH requests to update a series and invalidate cache.
        """
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            self._invalidate_series_cache()
            slug = kwargs.get("slug", "")
            async_to_sync(RedisService.delete)(f"series:slug:{slug}")
        return response

    @extend_schema(
        summary="Delete Series",
        description="Delete a racing series.",
        responses={
            204: OpenApiResponse(
                description="Series deleted successfully.",
            ),
            404: OpenApiResponse(
                description="Series not found.",
            ),
        },
    )
    def destroy(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle DELETE requests to remove a series and invalidate cache.
        """
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            self._invalidate_series_cache()
        return response


@extend_schema(tags=["Races"])
class RaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Race resources with Redis caching.

    Provides CRUD operations for individual races within a series.
    """

    queryset = Race.objects.select_related("series").all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["series", "status", "watch_platform"]
    search_fields = ["name"]
    ordering_fields = ["scheduled_at", "round_number", "status", "created_at"]
    ordering = ["-scheduled_at"]
    lookup_field = "slug"

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == "list":
            return RaceListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return RaceWriteSerializer
        return RaceDetailSerializer

    def _get_cache_key(self, request: DRFRequest, suffix: str = "") -> str:
        """Generate cache key for race requests."""
        key_parts = ["races"]

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

    def _invalidate_race_cache(self):
        """Invalidate all race-related cache."""
        async_to_sync(RedisService.delete_pattern)("races:*")
        async_to_sync(RedisService.delete_pattern)("race:slug:*")

    @extend_schema(
        summary="List Races",
        description="Retrieve a paginated list of all races with optional filtering.",
        responses={
            200: OpenApiResponse(
                description="Successful response with paginated race list.",
                response=RaceListSerializer,
            ),
        },
    )
    def list(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle GET requests to list all races with caching.
        """
        cache_key = self._get_cache_key(request, "list")

        cached_response = async_to_sync(RedisService.get)(cache_key)
        if cached_response:
            return cached_response

        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            async_to_sync(RedisService.set)(cache_key, response, timeout=300)

        return response

    @extend_schema(
        summary="Create Race",
        description="Create a new race.",
        request=RaceWriteSerializer,
        responses={
            201: OpenApiResponse(
                description="Race created successfully.",
                response=RaceDetailSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid input data.",
            ),
        },
    )
    def create(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle POST requests to create a new race and invalidate cache.
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            self._invalidate_race_cache()
        return response

    @extend_schema(
        summary="Retrieve Race",
        description="Retrieve a specific race by slug.",
        responses={
            200: OpenApiResponse(
                description="Successful response with race details.",
                response=RaceDetailSerializer,
            ),
            404: OpenApiResponse(
                description="Race not found.",
            ),
        },
    )
    def retrieve(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle GET requests to retrieve a specific race with caching.
        """
        slug = kwargs.get("slug", "")
        cache_key = f"race:slug:{slug}"

        cached_response = async_to_sync(RedisService.get)(cache_key)
        if cached_response:
            return cached_response

        response = super().retrieve(request, *args, **kwargs)

        if response.status_code == 200:
            async_to_sync(RedisService.set)(cache_key, response, timeout=600)

        return response

    @extend_schema(
        summary="Update Race",
        description="Update an existing race.",
        request=RaceWriteSerializer,
        responses={
            200: OpenApiResponse(
                description="Race updated successfully.",
                response=RaceDetailSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid input data.",
            ),
            404: OpenApiResponse(
                description="Race not found.",
            ),
        },
    )
    def update(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle PUT/PATCH requests to update a race and invalidate cache.
        """
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            self._invalidate_race_cache()
            slug = kwargs.get("slug", "")
            async_to_sync(RedisService.delete)(f"race:slug:{slug}")
        return response

    @extend_schema(
        summary="Delete Race",
        description="Delete a race.",
        responses={
            204: OpenApiResponse(
                description="Race deleted successfully.",
            ),
            404: OpenApiResponse(
                description="Race not found.",
            ),
        },
    )
    def destroy(self, request: DRFRequest, *args: Any, **kwargs: Any) -> Any:
        """
        Handle DELETE requests to remove a race and invalidate cache.
        """
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            self._invalidate_race_cache()
        return response
