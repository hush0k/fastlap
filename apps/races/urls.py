"""
URL configuration for the races app.
"""

# Django REST Framework
from rest_framework.routers import SimpleRouter

# Project modules
from apps.races.views import RaceViewSet, SeriesViewSet

router = SimpleRouter()
router.register("series", SeriesViewSet, basename="series")
router.register("", RaceViewSet, basename="races")

urlpatterns = router.urls