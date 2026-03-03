from typing import Any

from django_filters.rest_framework.backends import DjangoFilterBackend

from django.http import HttpRequest, HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.common.pagination import CustomPagination

from .filters import TournamentFilter
from .models import Tournament
from .serializers import TournamentListSerializer


class TournamentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TournamentListSerializer
    queryset = Tournament.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TournamentFilter
    pagination_class = CustomPagination


class TournamentView(APIView):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.method == "GET":
            handler = TournamentListView.as_view()
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return handler(request, *args, **kwargs)
