"""
ViewSet for the team_stuff app.
"""

# Python modules
from typing import Optional

# Django modules
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema

# Django REST Framework
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

# Project modules
from apps.common.services.redis_service import RedisService
from apps.team_stuff.models import StaffMember
from apps.team_stuff.serializers import (
    StaffMemberDetailSerializer,
    StaffMemberListSerializer,
    StaffMemberWriteSerializer,
    TeamRosterSerializer,
)


@extend_schema(tags=["Team Staff"])
class StaffMemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Staff Member resources with Redis caching.
    """

    queryset = StaffMember.objects.prefetch_related("rosters__team").all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["country", "role"]
    search_fields = ["first_name", "last_name", "role"]
    ordering_fields = ["last_name", "role", "country"]
    ordering = ["last_name"]

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action == "list":
            return StaffMemberListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return StaffMemberWriteSerializer
        return StaffMemberDetailSerializer

    def _get_cache_key(self, request: Request, suffix: str = "") -> str:
        """Generate cache key for staff requests."""
        key_parts = ["staff"]

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

    def _invalidate_staff_cache(self):
        """Invalidate all staff-related cache."""
        RedisService.delete_pattern("staff:*")
        RedisService.delete_pattern("staff:slug:*")
        RedisService.delete_pattern("staff:history:*")
        RedisService.delete_pattern("staff:current-team:*")

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle GET requests to list staff members with caching.
        """
        cache_key = self._get_cache_key(request, "list")

        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response

        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            RedisService.set(cache_key, response, timeout=300)

        return response

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle GET requests to retrieve a staff member with caching.
        """
        slug = kwargs.get("slug", "")
        cache_key = f"staff:slug:{slug}"

        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response

        response = super().retrieve(request, *args, **kwargs)

        if response.status_code == 200:
            RedisService.set(cache_key, response, timeout=600)

        return response

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST requests to create a staff member and invalidate cache.
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            self._invalidate_staff_cache()
        return response

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle PUT/PATCH requests to update a staff member and invalidate cache.
        """
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            self._invalidate_staff_cache()
        return response

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle DELETE requests to remove a staff member and invalidate cache.
        """
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            self._invalidate_staff_cache()
        return response

    @extend_schema(
        summary="Staff History",
        description="Team history for a staff member.",
        responses={
            200: OpenApiResponse(
                description="Successful response with staff history.",
                response=TeamRosterSerializer(many=True),
            ),
        },
    )
    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request: Request, slug: str | None = None) -> Response:
        """
        Team history for a staff member with caching.
        """
        cache_key = f"staff:history:{slug}"

        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response

        member: StaffMember = self.get_object()
        rosters = member.rosters.select_related("team").order_by("-start_date")
        serializer = TeamRosterSerializer(rosters, many=True)

        response = Response(serializer.data)
        RedisService.set(cache_key, response, timeout=300)

        return response

    @extend_schema(
        summary="Current Team",
        description="Current active team for a staff member.",
        responses={
            200: OpenApiResponse(
                description="Successful response with current team.",
                response=TeamRosterSerializer,
            ),
            404: OpenApiResponse(
                description="Staff member not assigned to any team.",
            ),
        },
    )
    @action(detail=True, methods=["get"], url_path="current-team")
    def current_team(self, request: Request, slug: str | None = None) -> Response:
        """
        Current active team for a staff member with caching.
        """
        cache_key = f"staff:current-team:{slug}"

        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response

        member: StaffMember = self.get_object()
        roster = member.rosters.filter(is_active=True).select_related("team").first()

        if not roster:
            return Response(
                {"detail": "Not currently assigned to any team."}, status=404
            )

        serializer = TeamRosterSerializer(roster)
        response = Response(serializer.data)
        RedisService.set(cache_key, response, timeout=300)

        return response
