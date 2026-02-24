from apps.common.models import BaseModel
from apps.common.mixins import NameMixin


class Tag(NameMixin, BaseModel):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        return self.name
