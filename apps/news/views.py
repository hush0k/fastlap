from logging import getLogger
from typing import Any

from django_filters.rest_framework.backends import DjangoFilterBackend

from django.http import HttpRequest, HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.common.pagination import CustomPagination

from .filters import ArticleFilter
from .models import Article
from .permissions import IsAuthor
from .serializers import (
    ArticleCreateSerializer,
    ArticleDestroySerializer,
    ArticleListSerializer,
    ArticleUpdateSerializer,
)

logger = getLogger(__name__)


class ArticleListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleListSerializer
    queryset = Article.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter


class ArticleCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = ArticleCreateSerializer


class ArticleUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = ArticleUpdateSerializer
    queryset = Article.objects.all()


class ArticleDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = ArticleDestroySerializer
    queryset = Article.objects.all()


class ArticleView(APIView):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.method == "GET":
            handler = ArticleListView.as_view()
        elif request.method == "POST":
            handler = ArticleCreateView.as_view()
        elif request.method == "PATCH":
            handler = ArticleUpdateView.as_view()
        elif request.method == "DELETE":
            handler = ArticleDestroyView.as_view()
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return handler(request, *args, **kwargs)
