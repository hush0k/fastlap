from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Article, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ArticleListSerializer(ModelSerializer):
    author = SerializerMethodField()
    tags = TagSerializer(many=True)
    series = SerializerMethodField()

    def get_series(self, obj: Article) -> list[dict[str, int | str]]:
        return [dict(id=i.id, name=i.name) for i in obj.series.all()]

    def get_author(self, obj: Article) -> dict[str, int | str]:
        return dict(id=obj.author.id, username=obj.author.username)

    class Meta:
        model = Article
        fields = "__all__"
