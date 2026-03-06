# apps/team_stuff/urls.py

from rest_framework.routers import DefaultRouter
from apps.team_stuff.views import StaffMemberViewSet

router = DefaultRouter()
router.register("staff", StaffMemberViewSet, basename="staff")

urlpatterns = router.urls