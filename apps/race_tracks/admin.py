"""
Admin configuration for the race_tracks app.
"""

# Django modules
from django.contrib import admin

# Project modules
from apps.race_tracks.models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
  """
  Admin interface for Track model.
  """

  list_display = (
    "id",
    "name",
    "slug",
    "country",
    "city",
    "timezone",
    "length_km",
    "lap_record",
    "lap_record_holder",
    "number_of_turns",
  )
  list_filter = ("country", "timezone")
  search_fields = ("name", "city", "country")
  readonly_fields = ("created_at", "updated_at", "slug")
  ordering = ("name", "country")
  fieldsets = (
    ("Basic Information", {
      "fields": ("name", "slug", "country", "city", "timezone")
    }),
    ("Track Specifications", {
      "fields": ("length_km", "number_of_turns", "map_image")
    }),
    ("Records", {
      "fields": ("lap_record", "lap_record_holder")
    }),
    ("Timestamps", {
      "fields": ("created_at", "updated_at"),
      "classes": ("collapse",)
    }),
  )