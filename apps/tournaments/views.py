"""
ViewSet for the tournaments app.
"""

# Python modules
from typing import Any

# Django modules
from django_filters.rest_framework import DjangoFilterBackend

# Django REST Framework
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse

# Project modules
from apps.common.pagination import CustomPagination
from apps.common.services.redis_service import RedisService
from apps.tournaments.filters import TournamentFilter
from apps.tournaments.models import Tournament
from apps.tournaments.permissions import IsContentManager
from apps.tournaments.serializers import (
    TournamentCreateSerializer,
    TournamentDetailSerializer,
    TournamentListSerializer,
    TournamentUpdateSerializer,
)


class TournamentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Tournament resources with Redis caching.
    """

    queryset = Tournament.objects.select_related("series")
    permission_classes = (IsAuthenticated, IsContentManager)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = TournamentFilter
    search_fields = ("name", "series__name")
    ordering_fields = ("year", "start_date", "end_date", "prize_fund", "total_rounds")
    ordering = ("-year", "-start_date")
    lookup_field = "slug"

    def get_permissions(self):
        """
        Set custom permissions for different actions.
        """
        if self.action in ("list", "retrieve"):
            return (AllowAny(),)
        return super().get_permissions()

    def get_queryset(self):
        """
        Filter queryset to show only active tournaments to non-authenticated users.
        """
        queryset = super().get_queryset()
        if self.action in ("list", "retrieve") and not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == "list":
            return TournamentListSerializer
        if self.action == "create":
            return TournamentCreateSerializer
        if self.action in ("update", "partial_update"):
            return TournamentUpdateSerializer
        return TournamentDetailSerializer

    def _get_cache_key(self, request: DRFRequest, suffix: str = "") -> str:
        """Generate cache key for tournament requests."""
        key_parts = ["tournaments"]
        
        query_params = request.GET.dict()
        if query_params:
            import json
            import hashlib
            params_hash = hashlib.md5(
                json.dumps(query_params, sort_keys=True).encode()
            ).hexdigest()[:8]
            key_parts.append(params_hash)
        
        offset = request.GET.get('offset', '0')
        limit = request.GET.get('limit', '20')
        key_parts.append(f"offset_{offset}")
        key_parts.append(f"limit_{limit}")
        
        if suffix:
            key_parts.append(suffix)
        
        return ":".join(key_parts)

    def _invalidate_tournament_cache(self):
        """Invalidate all tournament-related cache."""
        RedisService.delete_pattern("tournaments:*")
        RedisService.delete_pattern("tournament:slug:*")

    @extend_schema(
        summary="List Tournaments",
        description="Retrieve a paginated list of tournaments with optional filtering.",
        responses={
            200: OpenApiResponse(
                description="Successful response with paginated tournament list.",
                response=TournamentListSerializer,
            ),
        },
    )
    def list(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle GET requests to list all accessible tournaments with caching.
        """
        cache_key = self._get_cache_key(request, "list")
        
        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response
        
        response = super().list(request, *args, **kwargs)
        
        if response.status_code == 200:
            RedisService.set(cache_key, response, timeout=600)
        
        return response

    @extend_schema(
        summary="Create Tournament",
        description="Create a new tournament. User must be in ContentManager group.",
        request=TournamentCreateSerializer,
        responses={
            201: OpenApiResponse(
                description="Tournament created successfully.",
                response=TournamentDetailSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid input data.",
            ),
            403: OpenApiResponse(
                description="User is not authorized to create tournaments.",
            ),
        },
    )
    def create(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle POST requests to create a new tournament and invalidate cache.
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            self._invalidate_tournament_cache()
        return response

    @extend_schema(
        summary="Retrieve Tournament",
        description="Retrieve a specific tournament by slug.",
        responses={
            200: OpenApiResponse(
                description="Successful response with tournament details.",
                response=TournamentDetailSerializer,
            ),
            404: OpenApiResponse(
                description="Tournament not found.",
            ),
        },
    )
    def retrieve(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle GET requests to retrieve a specific tournament with caching.
        """
        slug = kwargs.get('slug', '')
        cache_key = f"tournament:slug:{slug}"
        
        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response
        
        response = super().retrieve(request, *args, **kwargs)
        
        if response.status_code == 200:
            RedisService.set(cache_key, response, timeout=600)
        
        return response

    @extend_schema(
        summary="Update Tournament",
        description="Update an existing tournament. User must be in ContentManager group.",
        request=TournamentUpdateSerializer,
        responses={
            200: OpenApiResponse(
                description="Tournament updated successfully.",
                response=TournamentDetailSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid input data.",
            ),
            403: OpenApiResponse(
                description="User is not authorized to update tournaments.",
            ),
            404: OpenApiResponse(
                description="Tournament not found.",
            ),
        },
    )
    def update(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle PUT/PATCH requests to update a tournament and invalidate cache.
        """
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            self._invalidate_tournament_cache()
        return response

    @extend_schema(
        summary="Delete Tournament",
        description="Delete a tournament. User must be in ContentManager group.",
        responses={
            204: OpenApiResponse(
                description="Tournament deleted successfully.",
            ),
            403: OpenApiResponse(
                description="User is not authorized to delete tournaments.",
            ),
            404: OpenApiResponse(
                description="Tournament not found.",
            ),
        },
    )
    def destroy(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle DELETE requests to remove a tournament and invalidate cache.
        """
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            self._invalidate_tournament_cache()
        return response