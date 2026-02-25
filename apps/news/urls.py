from django.urls import path

from .views import ArticleView

urlpatterns = [
    path("", ArticleView.as_view(), name="articles"),
    path("<int:pk>/", ArticleView.as_view(), name="article"),
]
