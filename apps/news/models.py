from logging import getLogger, Logger
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

from apps.common.utils import get_image_size_validator
from apps.common.mixins import NameMixin
from apps.common.models import BaseModel
from config.settings.base import (
    ARTICLE_IMAGE_MAX_SIZE_BYTES,
    ARTICLE_IMAGE_MAX_SIZE_MB,
    MEDIA_LOCATION,
)

logger: Logger = getLogger(__name__)


def article_cover_path(instance: "Article", filename: str) -> str:
    """Return upload path for an article cover using slug and original extension."""
    logger.debug("article: %s, filename: %s", instance.slug, filename)
    extension: str = Path(filename).suffix
    result: Path = MEDIA_LOCATION.ARTICLE_COVERS / (str(instance.slug) + extension)
    return str(result)

class Tag(NameMixin, BaseModel):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.id}, {self.name})"

validate_image_size = get_image_size_validator(ARTICLE_IMAGE_MAX_SIZE_BYTES)
class Article(BaseModel):
    name: CharField = CharField(max_length=255, validators=[MinLengthValidator(5)])
    slug: AutoSlugField = AutoSlugField(populate_from="name", unique=True)  # type: ignore[assignment]

    author: ForeignKey = ForeignKey(
        to="users.User",
        on_delete=CASCADE,
        related_name="articles",
        verbose_name=_("Author"),
    )
<<<<<<< HEAD
    content = TextField(
        verbose_name=_("Content"),
=======
    content: TextField = TextField(
        verbose_name="Content",
>>>>>>> 0e6107e1c089943cbfda7566fea209a804af52ae
        validators=[MinLengthValidator(200), MaxLengthValidator(7500)],
    )
    cover_image: ImageField = ImageField(
        upload_to=article_cover_path,
        blank=True,
        null=True,
        verbose_name=_("Cover Image"),
        validators=[validate_image_size],
    )
<<<<<<< HEAD
    series = ManyToManyField(
        to="races.Series", blank=True, related_name="articles", verbose_name=_("Series")
    )
    tags = ManyToManyField(to="news.Tag", related_name="articles", verbose_name=_("Tags"))  # noqa: E501
    published_at = DateTimeField(blank=True, null=True, verbose_name=_("Published At"))
    is_published = BooleanField(default=False, verbose_name=_("Is Published"))
    views_count = PositiveIntegerField(default=0, verbose_name=_("Views Count"))
=======
    series: ManyToManyField = ManyToManyField(
        to="races.Series", blank=True, related_name="articles", verbose_name="Series"
    )
    tags: ManyToManyField = ManyToManyField(
        to="news.Tag", related_name="articles", verbose_name="Tags"
    )
    published_at: DateTimeField = DateTimeField(blank=True, null=True, verbose_name="Published At")
    is_published: BooleanField = BooleanField(default=False, verbose_name="Is Published")
    views_count: PositiveIntegerField = PositiveIntegerField(default=0, verbose_name="Views Count")
>>>>>>> 0e6107e1c089943cbfda7566fea209a804af52ae

    author_id: int

    class Meta:
<<<<<<< HEAD
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

=======
        verbose_name = "Article"
        verbose_name_plural = "Articles"
>>>>>>> 0e6107e1c089943cbfda7566fea209a804af52ae
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.id}, {self.name})"