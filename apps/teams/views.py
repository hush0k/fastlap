"""
ViewSet for the teams app.
"""

# Python modules

# Django modules
from asgiref.sync import async_to_sync
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

# Django REST Framework
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

# Project modules
from apps.common.services.redis_service import RedisService
from apps.drivers.permissions import IsStaffOrReadOnly
from apps.teams.models import Team
from apps.teams.serializers import (
    TeamDetailSerializer,
    TeamListSerializer,
    TeamStandingsSerializer,
    TeamWriteSerializer,
)


@extend_schema(tags=["Teams"])
class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Team resources with Redis caching.
    """

    queryset = Team.objects.all().prefetch_related("standings__tournament")
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["name", "founded_year"]
    ordering = ["name"]
    search_fields = ["name", "short_name", "country"]
    filterset_fields = ["country", "founded_year"]

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action == "list":
            return TeamListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return TeamWriteSerializer
        return TeamDetailSerializer

    def _get_cache_key(self, request: Request, suffix: str = "") -> str:
        """Generate cache key for team requests."""
        key_parts = ["teams"]

        if request.user and request.user.is_authenticated:
            key_parts.append(f"user_{request.user.id}")

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

    def _invalidate_team_cache(self):
        """Invalidate all team-related cache."""
        async_to_sync(RedisService.delete_pattern)("teams:*")
        async_to_sync(RedisService.delete_pattern)("team:slug:*")
        async_to_sync(RedisService.delete_pattern)("team:standings:*")

    def list(self, request: Request, *args, **kwargs) -> Response:
        """List teams with caching."""
        cache_key = self._get_cache_key(request, "list")

        cached_response = async_to_sync(RedisService.get)(cache_key)
        if cached_response:
            return cached_response

        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            async_to_sync(RedisService.set)(cache_key, response, timeout=600)

        return response

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """Retrieve team with caching."""
        slug = kwargs.get("slug", "")
        cache_key = f"team:slug:{slug}"

        cached_response = async_to_sync(RedisService.get)(cache_key)
        if cached_response:
            return cached_response

        response = super().retrieve(request, *args, **kwargs)

        if response.status_code == 200:
            async_to_sync(RedisService.set)(cache_key, response, timeout=600)

        return response

    def create(self, request: Request, *args, **kwargs) -> Response:
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            self._invalidate_team_cache()
        return response

    def update(self, request: Request, *args, **kwargs) -> Response:
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            self._invalidate_team_cache()
        return response

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            self._invalidate_team_cache()
        return response

    @action(methods=["get"], detail=True, url_path="standings")
    def standings(self, request: Request, slug: str | None = None) -> Response:
        """Get team standings with caching."""
        cache_key = f"team:standings:{slug}"

        cached_response = async_to_sync(RedisService.get)(cache_key)
        if cached_response:
            return cached_response

        team = self.get_object()
        standings = team.standings.select_related("tournament").all()
        serializer = TeamStandingsSerializer(standings, many=True)

        response = Response(serializer.data)
        async_to_sync(RedisService.set)(cache_key, response, timeout=300)

        return response
