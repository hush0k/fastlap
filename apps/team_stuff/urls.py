# apps/team_stuff/urls.py

from rest_framework.routers import SimpleRouter

from apps.team_stuff.views import StaffMemberViewSet

router = SimpleRouter()
router.register("staff", StaffMemberViewSet, basename="staff")

urlpatterns = router.urls
