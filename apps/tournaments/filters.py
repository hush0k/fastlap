from django_filters import BaseInFilter, CharFilter, DateFilter, FilterSet, NumberFilter

from django.db.models import QuerySet

from .models import Tournament


class TournamentFilter(FilterSet):
    series = CharFilter(field_name="series__name")
    status = BaseInFilter(field_name="status")

    before = NumberFilter(field_name="year", lookup_expr="lt")
    after = NumberFilter(field_name="year", lookup_expr="gt")
    before_date = DateFilter(field_name="start_date", lookup_expr="lt")
    after_date = DateFilter(field_name="start_date", lookup_expr="gt")
    min_prize = NumberFilter(field_name="prize_fund", lookup_expr="gte")
    max_prize = NumberFilter(field_name="prize_fund", lookup_expr="lte")
    min_rounds = NumberFilter(field_name="total_rounds", lookup_expr="gte")
    max_rounds = NumberFilter(field_name="total_rounds", lookup_expr="lte")

    search = CharFilter(method="filter_search")

    def filter_search(
        self, queryset: QuerySet[Tournament], name: str, value: str
    ) -> QuerySet[Tournament]:
        return queryset.filter(name__icontains=value)

    class Meta:
        model = Tournament
        fields = ("slug", "year")
