from django.urls import path

from .views import ArticleDetailView, ArticleManageView, ArticleView

urlpatterns = [
    path("", ArticleView.as_view(), name="articles"),
    path("<int:pk>/", ArticleManageView.as_view(), name="article"),
    path("<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
]
