"""
Admin configuration for the team_stuff app.
"""

# Django modules
from django.contrib import admin

# Project modules
from apps.team_stuff.models import StaffMember, TeamRoster


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
  """
  Admin interface for StaffMember model.
  """

  list_display = (
    "id",
    "first_name",
    "last_name",
    "full_name",
    "role",
    "country",
    "age",
    "created_at",
  )
  list_filter = ("role", "country", "created_at")
  search_fields = ("first_name", "last_name", "role")
  readonly_fields = ("created_at", "updated_at", "slug")
  ordering = ("last_name", "first_name")
  fieldsets = (
    ("Personal Information", {
      "fields": ("first_name", "last_name", "slug", "age", "country")
    }),
    ("Professional Information", {
      "fields": ("role", "description", "photo")
    }),
    ("Timestamps", {
      "fields": ("created_at", "updated_at"),
      "classes": ("collapse",)
    }),
  )


@admin.register(TeamRoster)
class TeamRosterAdmin(admin.ModelAdmin):
  """
  Admin interface for TeamRoster model.
  """

  list_display = (
    "id",
    "team",
    "staff_member",
    "start_date",
    "end_date",
    "is_active",
  )
  list_filter = ("is_active", "team", "start_date")
  search_fields = ("team__name", "staff_member__first_name", "staff_member__last_name")
  readonly_fields = ("created_at", "updated_at")
  ordering = ("-start_date", "team")