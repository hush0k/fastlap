"""
URL configuration for the drivers app.
"""

# Django REST Framework
from rest_framework.routers import SimpleRouter

# Project modules
from apps.drivers.views import DriverResultViewSet, DriverViewSet

router = SimpleRouter()
router.register("", DriverViewSet, basename="drivers")
router.register("results", DriverResultViewSet, basename="driver-results")

urlpatterns = router.urls
