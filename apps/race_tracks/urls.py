from rest_framework.routers import SimpleRouter

from apps.race_tracks.views import RaceTrackViewSet

router = SimpleRouter()
router.register("tracks", RaceTrackViewSet, basename="track")

urlpatterns = router.urls
