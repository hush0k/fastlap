"""
Admin configuration for the drivers app.
"""

# Django modules
from django.contrib import admin

# Project modules
from apps.drivers.models import Driver, DriverResult


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
  """
  Admin interface for Driver model.
  """

  list_display = (
    "id",
    "first_name",
    "last_name",
    "slug",
    "nationality",
    "number",
    "is_active",
    "created_at",
  )
  list_filter = ("is_active", "nationality", "created_at")
  search_fields = ("first_name", "last_name", "slug")
  readonly_fields = ("created_at", "updated_at", "slug")
  ordering = ("last_name", "first_name")
  fieldsets = (
    ("Personal Information", {
      "fields": ("first_name", "last_name", "slug", "nationality", "date_of_birth")
    }),
    ("Racing Information", {
      "fields": ("number", "profile_image", "bio", "is_active")
    }),
    ("Timestamps", {
      "fields": ("created_at", "updated_at"),
      "classes": ("collapse",)
    }),
  )


@admin.register(DriverResult)
class DriverResultAdmin(admin.ModelAdmin):
  """
  Admin interface for DriverResult model.
  """

  list_display = (
    "id",
    "driver",
    "race",
    "position",
    "grid_position",
    "points",
    "status",
    "fastest_lap",
  )
  list_filter = ("status", "fastest_lap", "race__series")
  search_fields = ("driver__first_name", "driver__last_name", "race__name")
  readonly_fields = ("created_at", "updated_at")
  ordering = ("-race__scheduled_at", "position")