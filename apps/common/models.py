from django.db.models import Model


class BaseModel(Model):
    class Meta:
        abstract = True
    