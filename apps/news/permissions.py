from logging import getLogger, Logger

from django.utils.translation import gettext as _
from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .models import Article

logger: Logger = getLogger(__name__)


class IsAuthor(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        result: bool = request.user.groups.filter(name="Author").exists()
<<<<<<< HEAD
        logger.debug(_("user: %s, has_permission: %s"), request.user, result)

=======
        logger.debug("user: %s, has_permission: %s", request.user, result)
>>>>>>> 0e6107e1c089943cbfda7566fea209a804af52ae
        return result

    def has_object_permission(self, request: Request, view: View, obj: Article) -> bool:
        result: bool = obj.author_id == request.user.id
<<<<<<< HEAD

        logger.debug(_("user: %s, has_object_permission: %s"), request.user, result)
        return result
=======
        logger.debug("user: %s, has_object_permission: %s", request.user, result)
        return result
>>>>>>> 0e6107e1c089943cbfda7566fea209a804af52ae
