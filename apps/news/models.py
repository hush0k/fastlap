from pathlib import Path

from autoslug import AutoSlugField

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    PositiveIntegerField,
    TextField,
)

from apps.common.mixins import NameMixin
from apps.common.models import BaseModel
from config.settings.base import MEDIA_LOCATION


def article_cover_path(instance: "Article", filename: str) -> str:
    """Return upload path for an article cover using id and original extension."""

    extension = Path(filename).suffix
    result = MEDIA_LOCATION.ARTICLE_COVERS / (str(instance.id) + extension)

    return str(result)


class Tag(NameMixin, BaseModel):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        return self.name


class Article(BaseModel):
    name = CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)  # type: ignore

    author = ForeignKey(
        to="users.User",
        on_delete=CASCADE,
        related_name="articles",
        verbose_name="Author",
    )
    content = TextField(verbose_name="Content")
    cover_image = ImageField(
        upload_to=article_cover_path, blank=True, null=True, verbose_name="Cover Image"
    )
    series = ManyToManyField(
        to="races.Series", blank=True, related_name="articles", verbose_name="Series"
    )
    tags = ManyToManyField(to="news.Tag", related_name="articles", verbose_name="Tags")
    published_at = DateTimeField(blank=True, null=True, verbose_name="Published At")
    is_published = BooleanField(default=False, verbose_name="Is Published")
    views_count = PositiveIntegerField(default=0, verbose_name="Views Count")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.name
