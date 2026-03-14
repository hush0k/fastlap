from django.urls import path

from .views import TournamentView, TournamentDetailView

urlpatterns = [
    path("", TournamentView.as_view(), name="tournaments"),
    path("<int:pk>/", TournamentView.as_view(), name="tournament"),
    path("<int:pk>/detail/", TournamentDetailView.as_view(), name="tournament-detail"),
]
