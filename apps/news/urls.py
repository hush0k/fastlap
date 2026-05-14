"""
URL configuration for the news app.
"""

# Django REST Framework
from rest_framework.routers import SimpleRouter

# Project modules
from apps.news.views import ArticleViewSet

router = SimpleRouter()
router.register("", ArticleViewSet, basename="articles")

urlpatterns = router.urls
