from logging import getLogger
from pathlib import Path

from autoslug import AutoSlugField

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.core.validators import MaxLengthValidator, MinLengthValidator
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
from django.utils.translation import gettext_lazy as _

from apps.common.mixins import NameMixin
from apps.common.models import BaseModel
from config.settings.base import (
    ARTICLE_IMAGE_MAX_SIZE_BYTES,
    ARTICLE_IMAGE_MAX_SIZE_MB,
    MEDIA_LOCATION,
)

logger = getLogger(__name__)


def article_cover_path(instance: "Article", filename: str) -> str:
    """Return upload path for an article cover using id and original extension."""
    logger.debug("article: %s, filename: %s", instance.slug, filename)
    extension = Path(filename).suffix
    result = MEDIA_LOCATION.ARTICLE_COVERS / (str(instance.slug) + extension)

    return str(result)


def validate_image_size(value: UploadedFile):
    """:raises raise ValidationError:"""
    logger.debug("image size: %s", value.size)
    if value.size > (ARTICLE_IMAGE_MAX_SIZE_BYTES):
        raise ValidationError(f"Max image size is {ARTICLE_IMAGE_MAX_SIZE_MB} MB")


class Tag(NameMixin, BaseModel):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.id}, {self.name})"


class Article(BaseModel):
    name = CharField(max_length=255, validators=[MinLengthValidator(5)])
    slug = AutoSlugField(populate_from="name", unique=True)  # type: ignore

    author = ForeignKey(
        to="users.User",
        on_delete=CASCADE,
        related_name="articles",
        verbose_name=_("Author"),
    )
    content = TextField(
        verbose_name=_("Content"),
        validators=[MinLengthValidator(200), MaxLengthValidator(7500)],
    )
    cover_image = ImageField(
        upload_to=article_cover_path,
        blank=True,
        null=True,
        verbose_name=_("Cover Image"),
        validators=[validate_image_size],
    )
    series = ManyToManyField(
        to="races.Series", blank=True, related_name="articles", verbose_name=_("Series")
    )
    tags = ManyToManyField(to="news.Tag", related_name="articles", verbose_name=_("Tags"))  # noqa: E501
    published_at = DateTimeField(blank=True, null=True, verbose_name=_("Published At"))
    is_published = BooleanField(default=False, verbose_name=_("Is Published"))
    views_count = PositiveIntegerField(default=0, verbose_name=_("Views Count"))

    author_id: int

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

        ordering = ["-published_at"]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.id}, {self.name})"
