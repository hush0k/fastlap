from django_filters import (
    BaseInFilter,
    BooleanFilter,
    CharFilter,
    FilterSet,
    NumberFilter,
)

from django.db.models import Q, QuerySet

from .models import Driver, DriverResult


class DriverFilter(FilterSet):
    nationality = BaseInFilter(field_name="nationality")
    search = CharFilter(method="filter_search")
    is_active = BooleanFilter(field_name="is_active")
    number = NumberFilter(field_name="number")

    def filter_search(
        self, queryset: QuerySet[Driver], name: str, value: str
    ) -> QuerySet[Driver]:
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )

    class Meta:
        model = Driver
        fields = ["slug", "nationality", "is_active", "number"]


class DriverResultFilter(FilterSet):
    status = BaseInFilter(field_name="status")
    fastest_lap = BooleanFilter(field_name="fastest_lap")
    driver = NumberFilter(field_name="driver__id")
    race = NumberFilter(field_name="race__id")
    season = NumberFilter(field_name="race__season__id")
    series = NumberFilter(field_name="race__series__id")

    class Meta:
        model = DriverResult
        fields = ["driver", "race", "status", "fastest_lap", "season", "series"]
