from logging import Logger, getLogger
from typing import Any

from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from django.http import HttpRequest, HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.common.pagination import CustomPagination

from .filters import DriverFilter, DriverResultFilter
from .models import Driver, DriverResult
from .permissions import IsAdminOrReadOnly
from .serializers import (
    DriverDetailSerializer,
    DriverListSerializer,
    DriverResultCreateSerializer,
    DriverResultSerializer,
)

logger: Logger = getLogger(__name__)


@extend_schema(tags=["Drivers"])
class DriverListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DriverListSerializer
    queryset = Driver.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DriverFilter


@extend_schema(tags=["Drivers"])
class DriverCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = DriverDetailSerializer


@extend_schema(tags=["Drivers"])
class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = DriverDetailSerializer
    queryset = Driver.objects.all()
    lookup_field = "slug"


@extend_schema(tags=["Driver Results"])
class DriverResultListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DriverResultSerializer
    queryset = DriverResult.objects.select_related("driver", "race")
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DriverResultFilter


@extend_schema(tags=["Driver Results"])
class DriverResultCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = DriverResultCreateSerializer


class DriverView(APIView):
    @extend_schema(
        tags=["Drivers"],
        operation_id="v1_drivers_list",
        responses=DriverListSerializer,
    )
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = DriverListView.as_view()
        return handler(request, *args, **kwargs)

    @extend_schema(
        tags=["Drivers"],
        operation_id="v1_drivers_create",
        request=DriverDetailSerializer,
        responses=DriverDetailSerializer,
    )
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = DriverCreateView.as_view()
        return handler(request, *args, **kwargs)


class DriverResultView(APIView):
    @extend_schema(
        tags=["Driver Results"],
        operation_id="v1_driver_results_list",
        responses=DriverResultSerializer,
    )
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = DriverResultListView.as_view()
        return handler(request, *args, **kwargs)

    @extend_schema(
        tags=["Driver Results"],
        operation_id="v1_driver_results_create",
        request=DriverResultCreateSerializer,
        responses=DriverResultCreateSerializer,
    )
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = DriverResultCreateView.as_view()
        return handler(request, *args, **kwargs)
