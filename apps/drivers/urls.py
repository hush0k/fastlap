"""
URL configuration for the drivers app.
"""

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Project modules
from apps.drivers.views import DriverResultViewSet, DriverViewSet

router = DefaultRouter()
router.register("", DriverViewSet, basename="drivers")
router.register("results", DriverResultViewSet, basename="driver-results")

urlpatterns = router.urls