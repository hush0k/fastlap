from django.views import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAuthor(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.groups.filter(name="Author").exists()
