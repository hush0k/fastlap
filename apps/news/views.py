from typing import Any

from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

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
    ArticleDetailSerializer,
    ArticleListSerializer,
    ArticleUpdateSerializer,
)


@extend_schema(tags=["News"])
class ArticleListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleListSerializer
    queryset = (
        Article.objects.filter(is_published=True)
        .prefetch_related("tags", "series")
        .select_related("author")
    )
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter


@extend_schema(tags=["News"])
class ArticleCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = ArticleCreateSerializer


@extend_schema(tags=["News"])
class ArticleUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = ArticleUpdateSerializer
    queryset = Article.objects.all()


@extend_schema(tags=["News"])
class ArticleDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = ArticleDestroySerializer
    queryset = Article.objects.all()


@extend_schema(tags=["News"])
class ArticleDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleDetailSerializer
    queryset = (
        Article.objects.filter(is_published=True)
        .prefetch_related("tags", "series")
        .select_related("author")
    )
    lookup_field = "slug"


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