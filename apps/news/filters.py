from django_filters import BaseInFilter, CharFilter, DateFilter, FilterSet, NumberFilter

from django.db.models import QuerySet

from .models import Article


class ArticleFilter(FilterSet):
    series = BaseInFilter(field_name="series__name")
    tags = BaseInFilter(field_name="tags__name")
    search = CharFilter(method="filter_search")
    published_before = DateFilter(field_name="published_at", lookup_expr="lte")
    published_after = DateFilter(field_name="published_at", lookup_expr="gte")
    min_views = NumberFilter(field_name="views_count", lookup_expr="gte")
    max_views = NumberFilter(field_name="views_count", lookup_expr="lte")

    def filter_search(
        self, queryset: QuerySet[Article], name: str, value: str
    ) -> QuerySet[Article]:
        return queryset.filter(name__icontains=value)

    class Meta:
        model = Article
        fields = ["slug", "author_id"]
