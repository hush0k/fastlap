from django.db.models import Model, DateTimeField, CharField
from autoslug import AutoSlugField


class CreatedAtMixin(Model):
    created_at: DateTimeField = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtMixin(Model):
    updated_at: DateTimeField = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NameMixin(Model):
    name: CharField = CharField(max_length=255)
    slug: AutoSlugField = AutoSlugField(populate_from="name", unique=True, null=True, blank=True)

    class Meta:
        abstract = True