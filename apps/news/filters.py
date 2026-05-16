from django_filters import BaseInFilter, CharFilter, DateFilter, FilterSet, NumberFilter

from django.db.models import QuerySet

from .models import Article


class ArticleFilter(FilterSet):
    series: BaseInFilter = BaseInFilter(field_name="series__name")
    tags: BaseInFilter = BaseInFilter(field_name="tags__name")
    search: CharFilter = CharFilter(method="filter_search")
    published_before: DateFilter = DateFilter(
        field_name="published_at", lookup_expr="lte"
    )
    published_after: DateFilter = DateFilter(
        field_name="published_at", lookup_expr="gte"
    )
    min_views: NumberFilter = NumberFilter(field_name="views_count", lookup_expr="gte")
    max_views: NumberFilter = NumberFilter(field_name="views_count", lookup_expr="lte")

    def filter_search(
        self, queryset: QuerySet[Article], name: str, value: str
    ) -> QuerySet[Article]:
        return queryset.filter(name__icontains=value)

    class Meta:
        model = Article
        fields = ["slug", "author_id"]
