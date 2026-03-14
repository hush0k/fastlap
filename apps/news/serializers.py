from logging import getLogger
from typing import Any

from django.utils import timezone
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.races.models import Series
from apps.users.models import User

from .models import Article, Tag

logger = getLogger(__name__)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class ArticleListSerializer(ModelSerializer):
    author = SerializerMethodField()
    tags = TagSerializer(many=True)
    series = SerializerMethodField()

    def get_series(self, obj: Article) -> list[dict[str, int | str]]:
        return [dict(id=i.id, name=i.name) for i in obj.series.all()]

    def get_author(self, obj: Article) -> dict[str, int | str]:
        return dict(id=obj.author.id, username=obj.author.username)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleDetailSerializer(ModelSerializer):
    author = SerializerMethodField()
    tags = TagSerializer(many=True)
    series = SerializerMethodField()

    def get_series(self, obj: Article) -> list[dict[str, int | str]]:
        return [dict(id=i.id, name=i.name) for i in obj.series.all()]

    def get_author(self, obj: Article) -> dict[str, int | str]:
        return dict(
            id=obj.author.id,
            username=obj.author.username,
            first_name=obj.author.first_name,
            last_name=obj.author.last_name,
        )

    class Meta:
        model = Article
        fields = [
            "id",
            "name",
            "slug",
            "author",
            "content",
            "cover_image",
            "series",
            "tags",
            "published_at",
            "is_published",
            "views_count",
        ]


class ArticleCreateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("id", "slug", "author", "views_count", "published_at")

    def create(self, validated_data: dict[str, Any]) -> Article:
        user: User = self.context["request"].user
        logger.debug("create user=%s, data=%r", user, validated_data)

        tags: list[Tag] = validated_data.pop("tags", [])
        series: list[Series] = validated_data.pop("series", [])

        if validated_data["is_published"] is True:
            validated_data["published_at"] = timezone.now()
            logger.debug("published_at was set")

        article = Article.objects.create(author=user, **validated_data)

        article.tags.set(tags)
        article.series.set(series)
        logger.debug("tags and series was assigned")

        logger.info("created article: %s", article.id)
        return article


class ArticleUpdateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("id", "slug", "author", "views_count", "published_at")

    def update(self, instance: Article, validated_data: Any) -> Article:
        logger.debug("validated_data: %r", validated_data)

        if validated_data.get("is_published") is True and instance.published_at is None:
            validated_data["published_at"] = timezone.now()
            logger.debug("article %s: published_at assigned", instance.id)

        result = super().update(instance, validated_data)
        logger.info("updated article: %s", result.id)

        return result


class ArticleDestroySerializer(ModelSerializer):
    class Meta:
        model = Article
