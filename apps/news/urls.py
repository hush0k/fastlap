"""
URL configuration for the news app.
"""

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Project modules
from apps.news.views import ArticleViewSet

router = DefaultRouter()
router.register("", ArticleViewSet, basename="articles")

urlpatterns = router.urls