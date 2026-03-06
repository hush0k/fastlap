
from rest_framework.routers import DefaultRouter
from apps.race_tracks.views import RaceTrackViewSet

router = DefaultRouter()
router.register("tracks", RaceTrackViewSet, basename="track")

urlpatterns = router.urls