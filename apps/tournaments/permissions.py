from logging import getLogger

from django.utils.translation import gettext as _
from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from apps.common.enums import RoleEnum

logger = getLogger(__name__)


class IsContentManager(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
<<<<<<< HEAD
        result: bool = request.user.groups.filter(name="ContentManager").exists()
        logger.debug(_("user: %s, has_permission: %s"), request.user, result)
=======
        result: bool = request.user.groups.filter(name=RoleEnum.CONTENT_MANAGER).exists()
        logger.debug("user: %s, has_permission: %s", request.user, result)
>>>>>>> e352d4a8f3d9b40780960780cf8ad99fc02abb18

        return result
