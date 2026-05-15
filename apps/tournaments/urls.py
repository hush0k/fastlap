from django.urls import path

from .views import TournamentDetailView, TournamentManageView, TournamentView

urlpatterns = [
    path("", TournamentView.as_view(), name="tournaments"),
    path("<int:pk>/", TournamentManageView.as_view(), name="tournament"),
    path("<int:pk>/detail/", TournamentDetailView.as_view(), name="tournament-detail"),
]
