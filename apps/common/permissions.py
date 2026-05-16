from django.views import View
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request


class IsAuthenticatedReadOnlyOrStaffWrite(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return bool(user.is_staff)
