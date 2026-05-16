from logging import getLogger

from django.utils.translation import gettext as _
from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from apps.common.enums import RoleEnum

logger = getLogger(__name__)


class IsContentManager(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        result: bool = request.user.groups.filter(
            name=RoleEnum.CONTENT_MANAGER
        ).exists()
        logger.debug(_("user: %s, has_permission: %s"), request.user, result)

        return result
