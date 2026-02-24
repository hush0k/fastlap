from logging import getLogger

from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.common.pagination import CustomPagination

from .models import Article
from .serializers import ArticleListSerializer

logger = getLogger(__name__)


class ArticleListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ArticleListSerializer
    queryset = Article.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self) -> QuerySet[Article]:
        q = Article.objects.all()

        author_id: str | None = self.request.query_params.get("author_id")
        logger.debug("author_id: %r", author_id)
        if author_id is not None and author_id.isdigit():
            q = q.filter(author_id=int(author_id))

        series: list[str] = self.request.query_params.getlist("series")
        logger.debug("series: %r", series)
        if series:
            q = q.filter(series__name__in=series)

        return q
