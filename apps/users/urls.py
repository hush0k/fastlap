from django.urls import path

from .views import LoginView, RefreshView, RegisterView
from .vieews.avatar_views import upload_avatar, get_avatar, delete_avatar

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
    path("avatar/upload/", upload_avatar, name="upload_avatar"),
    path("avatar/", get_avatar, name="get_avatar"),
    path("avatar/delete/", delete_avatar, name="delete_avatar"),
]
