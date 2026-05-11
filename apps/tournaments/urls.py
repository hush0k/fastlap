"""
URL configuration for the tournaments app.
"""

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Project modules
from apps.tournaments.views import TournamentViewSet

router = DefaultRouter()
router.register("", TournamentViewSet, basename="tournaments")

urlpatterns = router.urls