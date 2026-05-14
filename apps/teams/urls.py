from rest_framework.routers import SimpleRouter

from apps.teams.views import TeamViewSet

router = SimpleRouter()
router.register("", TeamViewSet, basename="teams")

urlpatterns = router.urls
