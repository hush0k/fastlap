"""
Admin configuration for the tournaments app.
"""

# Django modules
from django.contrib import admin

# Project modules
from apps.tournaments.models import DriverStanding, TeamStanding, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """
    Admin interface for Tournament model.
    """

    list_display = (
        "id",
        "name",
        "slug",
        "series",
        "year",
        "status",
        "is_active",
        "start_date",
        "end_date",
        "total_rounds",
        "prize_fund",
        "currency",
    )
    list_filter = ("status", "is_active", "series", "year")
    search_fields = ("name", "slug", "series__name")
    readonly_fields = ("created_at", "updated_at", "slug")
    ordering = ("-year", "-start_date")
    date_hierarchy = "start_date"
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "slug", "series", "year", "status", "is_active")},
        ),
        ("Media", {"fields": ("logo",), "classes": ("collapse",)}),
        ("Dates & Rounds", {"fields": ("start_date", "end_date", "total_rounds")}),
        ("Financial", {"fields": ("prize_fund", "currency")}),
        (
            "Additional",
            {"fields": ("description", "regulations_url"), "classes": ("collapse",)},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(TeamStanding)
class TeamStandingAdmin(admin.ModelAdmin):
    """
    Admin interface for TeamStanding model.
    """

    list_display = ("id", "team", "tournament", "position", "points")
    list_filter = ("tournament",)
    search_fields = ("team__name", "tournament__name")
    ordering = ("tournament", "position")


@admin.register(DriverStanding)
class DriverStandingAdmin(admin.ModelAdmin):
    """
    Admin interface for DriverStanding model.
    """

    list_display = ("id", "driver", "tournament", "position", "points")
    list_filter = ("tournament",)
    search_fields = ("driver__first_name", "driver__last_name", "tournament__name")
    ordering = ("tournament", "position")
