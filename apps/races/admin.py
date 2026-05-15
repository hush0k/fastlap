"""
Admin configuration for the races app.
"""

# Django modules
from django.contrib import admin

# Project modules
from apps.races.models import Race, Series


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    """
    Admin interface for Series model.
    """

    list_display = ["id", "name", "slug", "category", "created_at"]
    list_filter = ["category", "created_at"]
    search_fields = ["name", "slug", "description"]
    readonly_fields = ["created_at", "updated_at", "slug"]
    ordering = ["name"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "category", "description")}),
        ("Media", {"fields": ("logo",), "classes": ("collapse",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    """
    Admin interface for Race model.
    """

    list_display = [
        "id",
        "name",
        "slug",
        "series",
        "round_number",
        "scheduled_at",
        "status",
        "watch_platform",
    ]
    list_filter = ["status", "watch_platform", "series", "scheduled_at"]
    search_fields = ["name", "slug", "series__name"]
    readonly_fields = ["created_at", "updated_at", "slug"]
    ordering = ["-scheduled_at"]
    date_hierarchy = "scheduled_at"

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "slug", "series", "round_number", "status")},
        ),
        ("Schedule", {"fields": ("scheduled_at",)}),
        ("Race Details", {"fields": ("laps_total",)}),
        ("Broadcast", {"fields": ("watch_platform", "watch_url")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
