"""
ViewSet for the races app.
"""

# Python modules
from typing import Any

# Django modules
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema

# Django REST Framework
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request as DRFRequest

# Project modules
from apps.common.pagination import CustomPagination
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
    ViewSet for managing Series resources.

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
        Handle GET requests to list all series.
        """
        return super().list(request, *args, **kwargs)

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
        Handle POST requests to create a new series.
        """
        return super().create(request, *args, **kwargs)

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
        Handle GET requests to retrieve a specific series.
        """
        return super().retrieve(request, *args, **kwargs)

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
        Handle PUT/PATCH requests to update a series.
        """
        return super().update(request, *args, **kwargs)

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
        Handle DELETE requests to remove a series.
        """
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["Races"])
class RaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Race resources.

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
        Handle GET requests to list all races.
        """
        return super().list(request, *args, **kwargs)

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
        Handle POST requests to create a new race.
        """
        return super().create(request, *args, **kwargs)

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
        Handle GET requests to retrieve a specific race.
        """
        return super().retrieve(request, *args, **kwargs)

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
        Handle PUT/PATCH requests to update a race.
        """
        return super().update(request, *args, **kwargs)

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
        Handle DELETE requests to remove a race.
        """
        return super().destroy(request, *args, **kwargs)
