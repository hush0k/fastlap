from django.urls import path

from .views import DriverDetailView, DriverResultView, DriverView

urlpatterns = [
    path("", DriverView.as_view(), name="driver-list-create"),
    path("results/", DriverResultView.as_view(), name="driver-result-list-create"),
    path("<slug:slug>/", DriverDetailView.as_view(), name="driver-detail"),
]
