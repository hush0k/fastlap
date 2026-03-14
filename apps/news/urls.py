from django.urls import path

from .views import ArticleView, ArticleDetailView

urlpatterns = [
    path("", ArticleView.as_view(), name="articles"),
    path("<int:pk>/", ArticleView.as_view(), name="article"),
    path("<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
]
