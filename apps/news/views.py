"""
ViewSet for the news app.
"""

# Python modules
from typing import Any

# Django modules
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse

# Project modules
from apps.common.pagination import CustomPagination
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
    ViewSet for managing Article resources.
    """

    queryset = Article.objects.prefetch_related("tags", "series").select_related("author")
    permission_classes = (IsAuthenticated, IsAuthor)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
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

        if self.action in ("list", "retrieve") and not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        return queryset

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
        Handle GET requests to list all accessible articles.
        """
        return super().list(request, *args, **kwargs)

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
        Handle POST requests to create a new article.
        """
        return super().create(request, *args, **kwargs)

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
        Handle GET requests to retrieve a specific article.
        """
        article: Article = self.get_object()
        article.views_count += 1
        article.save(update_fields=["views_count"])
        serializer = self.get_serializer(article)
        return DRFResponse(serializer.data)

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
        Handle PUT/PATCH requests to update an article.
        """
        return super().update(request, *args, **kwargs)

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
        Handle DELETE requests to remove an article.
        """
        return super().destroy(request, *args, **kwargs)

    @action(
        methods=("GET",),
        detail=False,
        url_path="my-articles",
        url_name="my-articles",
        permission_classes=(IsAuthenticated, IsAuthor),
    )
    def my_articles(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Retrieve articles authored by the authenticated user.
        """
        articles = Article.objects.filter(author=request.user).prefetch_related(
            "tags", "series"
        ).select_related("author")
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ArticleListSerializer(articles, many=True)
        return DRFResponse(serializer.data)