from logging import Logger, getLogger

from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .models import Article

logger: Logger = getLogger(__name__)


class IsAuthor(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        result: bool = request.user.groups.filter(name="Author").exists()
        logger.debug("user: %s, has_permission: %s", request.user, result)
        return result

    def has_object_permission(self, request: Request, view: View, obj: Article) -> bool:
        result: bool = obj.author_id == request.user.id
        logger.debug("user: %s, has_object_permission: %s", request.user, result)
        return result
