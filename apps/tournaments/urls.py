"""
URL configuration for the tournaments app.
"""

# Django REST Framework
from rest_framework.routers import SimpleRouter

# Project modules
from apps.tournaments.views import TournamentViewSet

router = SimpleRouter()
router.register("", TournamentViewSet, basename="tournaments")

urlpatterns = router.urls
