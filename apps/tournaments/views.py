from typing import Any

from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from django.http import HttpRequest, HttpResponse
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.common.pagination import CustomPagination

from .filters import TournamentFilter
from .models import Tournament
from .permissions import IsContentManager
from .serializers import (
    TournamentCreateSerializer,
    TournamentDetailSerializer,
    TournamentListSerializer,
    TournamentUpdateSerializer,
)


@extend_schema(tags=["Tournaments"])
class TournamentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TournamentListSerializer
    queryset = Tournament.objects.filter(is_active=True).select_related("series")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TournamentFilter
    search_fields = ["name", "series__name"]
    pagination_class = CustomPagination


@extend_schema(tags=["Tournaments"])
class TournamentDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = TournamentDetailSerializer
    queryset = Tournament.objects.filter(is_active=True).select_related("series")


@extend_schema(tags=["Tournaments"])
class TournamentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsContentManager]
    serializer_class = TournamentCreateSerializer


@extend_schema(tags=["Tournaments"])
class TournamentUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsContentManager]
    serializer_class = TournamentUpdateSerializer
    queryset = Tournament.objects.all()


@extend_schema(tags=["Tournaments"])
class TournamentDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsContentManager]
    queryset = Tournament.objects.all()


class TournamentView(APIView):
    @extend_schema(
        tags=["Tournaments"],
        operation_id="v1_tournaments_list",
        responses=TournamentListSerializer,
    )
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = TournamentListView.as_view()
        return handler(request, *args, **kwargs)

    @extend_schema(
        tags=["Tournaments"],
        operation_id="v1_tournaments_create",
        request=TournamentCreateSerializer,
        responses=TournamentDetailSerializer,
    )
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = TournamentCreateView.as_view()
        return handler(request, *args, **kwargs)


class TournamentManageView(APIView):
    @extend_schema(
        tags=["Tournaments"],
        operation_id="v1_tournaments_update",
        request=TournamentUpdateSerializer,
        responses=TournamentDetailSerializer,
    )
    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = TournamentUpdateView.as_view()
        return handler(request, *args, **kwargs)

    @extend_schema(
        tags=["Tournaments"],
        operation_id="v1_tournaments_partial_update",
        request=TournamentUpdateSerializer,
        responses=TournamentDetailSerializer,
    )
    def patch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = TournamentUpdateView.as_view()
        return handler(request, *args, **kwargs)

    @extend_schema(
        tags=["Tournaments"],
        operation_id="v1_tournaments_destroy",
        responses={204: None},
    )
    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = TournamentDestroyView.as_view()
        return handler(request, *args, **kwargs)
