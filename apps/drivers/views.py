"""
ViewSet for the drivers app.
"""

# Python modules
from typing import Any

# Django modules
from django_filters.rest_framework import DjangoFilterBackend

# Django REST Framework
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse

# Project modules
from apps.common.pagination import CustomPagination
from apps.common.decorators.cache_decorators import cache_response, invalidate_cache
from apps.drivers.filters import DriverFilter, DriverResultFilter
from apps.drivers.models import Driver, DriverResult
from apps.drivers.permissions import IsAdminOrReadOnly
from apps.drivers.serializers import (
    DriverDetailSerializer,
    DriverListSerializer,
    DriverResultCreateSerializer,
    DriverResultSerializer,
)


class DriverViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Driver resources.
    """

    queryset = Driver.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    lookup_field = "slug"
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = DriverFilter
    search_fields = ("first_name", "last_name")
    ordering_fields = ("first_name", "last_name", "number")
    ordering = ("last_name", "first_name")

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == "list":
            return DriverListSerializer
        return DriverDetailSerializer

    @extend_schema(
        summary="List Drivers",
        description="Retrieve a paginated list of all drivers with optional filtering.",
        responses={
            200: OpenApiResponse(
                description="Successful response with paginated driver list.",
                response=DriverListSerializer,
            ),
        },
    )
    def list(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle GET requests to list all drivers.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve Driver Details",
        description="Retrieve detailed information about a specific driver by slug.",
        responses={
            200: OpenApiResponse(
                description="Successful response with driver details.",
                response=DriverDetailSerializer,
            ),
            404: OpenApiResponse(
                description="Driver not found with the provided slug.",
            ),
        },
    )
    def retrieve(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle GET requests to retrieve a specific driver.
        """
        return super().retrieve(request, *args, **kwargs)

    @action(
        methods=("GET",),
        detail=True,
        url_path="results",
        url_name="results",
        permission_classes=(AllowAny,),
    )
    def results(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Retrieve race results for a specific driver.
        """
        driver: Driver = self.get_object()
        results = DriverResult.objects.filter(driver=driver).select_related("race")
        serializer = DriverResultSerializer(results, many=True)
        return DRFResponse(serializer.data)
    
    @cache_response(timeout=300, key_prefix='drivers_list')
    def list(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle GET requests to list all drivers with caching.
        """
        return super().list(request, *args, **kwargs)
    
    @invalidate_cache('drivers_list:*')
    def create(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle POST requests to create a new driver (invalidates cache).
        """
        return super().create(request, *args, **kwargs)
    
    @invalidate_cache('drivers_list:*')
    def update(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle PUT/PATCH requests to update a driver (invalidates cache).
        """
        return super().update(request, *args, **kwargs)
    
    @invalidate_cache('drivers_list:*')
    def destroy(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle DELETE requests to remove a driver (invalidates cache).
        """
        return super().destroy(request, *args, **kwargs)


class DriverResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing DriverResult resources.
    """

    queryset = DriverResult.objects.select_related("driver", "race")
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = DriverResultFilter
    ordering_fields = ("position", "points", "race__scheduled_at")
    ordering = ("race__scheduled_at", "position")

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action in ("create", "update", "partial_update"):
            return DriverResultCreateSerializer
        return DriverResultSerializer