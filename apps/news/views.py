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
    @extend_schema(
        tags=["News"],
        operation_id="v1_news_list",
        responses=ArticleListSerializer,
    )
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = ArticleListView.as_view()
        return handler(request, *args, **kwargs)

    @extend_schema(
        tags=["News"],
        operation_id="v1_news_create",
        request=ArticleCreateSerializer,
        responses=ArticleDetailSerializer,
    )
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = ArticleCreateView.as_view()
        return handler(request, *args, **kwargs)


class ArticleManageView(APIView):
    @extend_schema(
        tags=["News"],
        operation_id="v1_news_partial_update",
        request=ArticleUpdateSerializer,
        responses=ArticleDetailSerializer,
    )
    def patch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = ArticleUpdateView.as_view()
        return handler(request, *args, **kwargs)

    @extend_schema(tags=["News"], operation_id="v1_news_destroy", responses={204: None})
    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        handler = ArticleDestroyView.as_view()
        return handler(request, *args, **kwargs)
