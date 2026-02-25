from logging import getLogger

from django_filters.rest_framework.backends import DjangoFilterBackend

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.common.pagination import CustomPagination

from .filters import ArticleFilter
from .models import Article
from .serializers import ArticleListSerializer

logger = getLogger(__name__)


class ArticleListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ArticleListSerializer
    queryset = Article.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter
