from logging import getLogger
from typing import Any

from django_filters.rest_framework.backends import DjangoFilterBackend

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

logger = getLogger(__name__)


class DriverListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DriverListSerializer
    queryset = Driver.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DriverFilter


class DriverCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = DriverDetailSerializer


class DriverView(APIView):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.method == "GET":
            handler = DriverListView.as_view()
        elif request.method == "POST":
            handler = DriverCreateView.as_view()
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)
        return handler(request, *args, **kwargs)


class DriverDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DriverDetailSerializer
    queryset = Driver.objects.all()
    lookup_field = "slug"


class DriverResultListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DriverResultSerializer
    queryset = DriverResult.objects.select_related("driver", "race")
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DriverResultFilter


class DriverResultCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = DriverResultCreateSerializer


class DriverResultView(APIView):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.method == "GET":
            handler = DriverResultListView.as_view()
        elif request.method == "POST":
            handler = DriverResultCreateView.as_view()
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)
        return handler(request, *args, **kwargs)
