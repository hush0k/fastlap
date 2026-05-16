"""
ViewSet for the news app.
"""

# Python modules
from typing import Any

# Django modules
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema

from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse

# Project modules
from apps.common.pagination import CustomPagination
from apps.common.services.redis_service import RedisService
from apps.news.filters import ArticleFilter
from apps.news.models import Article
from apps.news.permissions import IsAuthor
from apps.news.serializers import (
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
    ArticleUpdateSerializer,
)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Article resources with Redis caching.
    """

    queryset = Article.objects.prefetch_related("tags", "series").select_related(
        "author"
    )
    permission_classes = (IsAuthenticated, IsAuthor)
    pagination_class = CustomPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = ArticleFilter
    search_fields = ("name", "content")
    ordering_fields = ("published_at", "views_count", "created_at")
    ordering = ("-published_at",)
    lookup_field = "slug"

    def get_permissions(self):
        """
        Set custom permissions for different actions.
        """
        if self.action in ("list", "retrieve"):
            return (AllowAny(),)
        return super().get_permissions()

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == "list":
            return ArticleListSerializer
        if self.action == "create":
            return ArticleCreateSerializer
        if self.action in ("update", "partial_update"):
            return ArticleUpdateSerializer
        return ArticleDetailSerializer

    def get_queryset(self):
        """
        Filter queryset based on user permissions and action.
        """
        queryset = super().get_queryset()

        if (
            self.action in ("list", "retrieve")
            and not self.request.user.is_authenticated
        ):
            queryset = queryset.filter(is_published=True)

        return queryset

    def _get_list_cache_key(self, request: DRFRequest) -> str:
        """Generate cache key for article list."""
        key_parts = ["news", "list"]

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

        return ":".join(key_parts)

    def _invalidate_news_cache(self):
        """Invalidate all news-related cache."""
        RedisService.delete_pattern("news:*")
        RedisService.delete_pattern("article:slug:*")

    @extend_schema(
        summary="List Articles",
        description="Retrieve a paginated list of articles with optional filtering.",
        responses={
            200: OpenApiResponse(
                description="Successful response with paginated article list.",
                response=ArticleListSerializer,
            ),
        },
    )
    def list(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle GET requests to list all accessible articles with caching.
        """
        cache_key = self._get_list_cache_key(request)

        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response

        response = super().list(request, *args, **kwargs)

        if response.status_code == 200:
            RedisService.set(cache_key, response, timeout=300)

        return response

    @extend_schema(
        summary="Create Article",
        description="Create a new article. User must be in Author group.",
        request=ArticleCreateSerializer,
        responses={
            201: OpenApiResponse(
                description="Article created successfully.",
                response=ArticleDetailSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid input data.",
            ),
            403: OpenApiResponse(
                description="User is not authorized to create articles.",
            ),
        },
    )
    def create(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle POST requests to create a new article and invalidate cache.
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            self._invalidate_news_cache()
        return response

    @extend_schema(
        summary="Retrieve Article",
        description="Retrieve a specific article by slug.",
        responses={
            200: OpenApiResponse(
                description="Successful response with article details.",
                response=ArticleDetailSerializer,
            ),
            404: OpenApiResponse(
                description="Article not found.",
            ),
        },
    )
    def retrieve(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle GET requests to retrieve a specific article with caching.
        """
        slug = kwargs.get("slug", "")
        cache_key = f"article:slug:{slug}"

        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response

        article: Article = self.get_object()
        article.views_count += 1
        article.save(update_fields=["views_count"])

        serializer = self.get_serializer(article)
        response = DRFResponse(serializer.data)

        RedisService.set(cache_key, response, timeout=600)

        return response

    @extend_schema(
        summary="Update Article",
        description="Update an existing article. User must be the author.",
        request=ArticleUpdateSerializer,
        responses={
            200: OpenApiResponse(
                description="Article updated successfully.",
                response=ArticleDetailSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid input data.",
            ),
            403: OpenApiResponse(
                description="User is not the author of this article.",
            ),
            404: OpenApiResponse(
                description="Article not found.",
            ),
        },
    )
    def update(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle PUT/PATCH requests to update an article and invalidate cache.
        """
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            self._invalidate_news_cache()
            slug = kwargs.get("slug", "")
            RedisService.delete(f"article:slug:{slug}")
        return response

    @extend_schema(
        summary="Delete Article",
        description="Delete an article. User must be the author.",
        responses={
            204: OpenApiResponse(
                description="Article deleted successfully.",
            ),
            403: OpenApiResponse(
                description="User is not the author of this article.",
            ),
            404: OpenApiResponse(
                description="Article not found.",
            ),
        },
    )
    def destroy(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle DELETE requests to remove an article and invalidate cache.
        """
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            self._invalidate_news_cache()
        return response

    @extend_schema(
        summary="My Articles",
        description="Retrieve articles authored by the authenticated user.",
        responses={
            200: OpenApiResponse(
                description="Successful response with user's articles.",
                response=ArticleListSerializer,
            ),
        },
    )
    @action(
        methods=("GET",),
        detail=False,
        url_path="my-articles",
        url_name="my-articles",
        permission_classes=(IsAuthenticated, IsAuthor),
    )
    def my_articles(
        self, request: DRFRequest, *args: Any, **kwargs: Any
    ) -> DRFResponse:
        """
        Retrieve articles authored by the authenticated user with caching.
        """
        cache_key = f"news:my_articles:user_{request.user.id}"

        cached_response = RedisService.get(cache_key)
        if cached_response:
            return cached_response

        articles = (
            Article.objects.filter(author=request.user)
            .prefetch_related("tags", "series")
            .select_related("author")
        )
        page = self.paginate_queryset(articles)

        if page is not None:
            serializer = ArticleListSerializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
        else:
            serializer = ArticleListSerializer(articles, many=True)
            response = DRFResponse(serializer.data)

        RedisService.set(cache_key, response, timeout=60)

        return response
