"""
URL configuration for the users app.
"""

# Django modules
from django.urls import path

# Django REST Framework
from rest_framework.routers import SimpleRouter

# Project modules
from apps.users.views import LoginView, RefreshView, RegisterView
from apps.users.viewsets.avatar_viewset import AvatarViewSet

router = SimpleRouter()
router.register("avatar", AvatarViewSet, basename="avatar")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
