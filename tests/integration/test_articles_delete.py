from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from apps.news.models import Article, Tag
from apps.races.models import Series
from tests.config import (
    IMAGE_PATH,
    TEST_LOGGER_NAME,
)
from tests.utils import (
    get_simple_upload_file,
    get_user,
)

logger = getLogger(TEST_LOGGER_NAME)


class TestArticleDelete(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.series_f1 = Series.objects.create(name="Formula 1", category="car")
        cls.series_nascar = Series.objects.create(name="NASCAR", category="car")

        cls.tag_race = Tag.objects.create(name="Race")
        cls.tag_qualifying = Tag.objects.create(name="Qualifying")

        cls.author_group = Group.objects.get_or_create(name="Author")[0]

        cls.ordinary_user = get_user()
        cls.author1 = get_user(email="author1@example.com", username="author1")
        cls.author2 = get_user(email="author2@example.com", username="author2")
        cls.author1.groups.add(cls.author_group)
        cls.author2.groups.add(cls.author_group)

        cls.access_token = str(AccessToken.for_user(cls.author1))

    def setUp(self) -> None:
        self.article = Article.objects.create(
            name="Title",
            author=self.author1,
            content="a" * 255,
            is_published=True,
            cover_image=get_simple_upload_file(IMAGE_PATH),
        )
        self.article.series.add(self.series_f1)
        self.article.series.add(self.series_nascar)
        self.article.tags.add(self.tag_race)
        self.article_url = reverse(
            "articles-detail", kwargs={"slug": self.article.slug}
        )

    def test_success_delete(self) -> None:
        response = self.client.delete(
            self.article_url, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Article.objects.filter(author=self.author1).exists())

    def test_delete_nonexistent_article(self) -> None:
        self.client.delete(
            self.article_url, headers={"Authorization": f"Bearer {self.access_token}"}
        )

        response = self.client.delete(
            self.article_url, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 404)

    def test_delete_another_author_article_not_allowed(self) -> None:
        response = self.client.delete(
            self.article_url,
            headers={"Authorization": f"Bearer {AccessToken.for_user(self.author2)}"},
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Article.objects.filter(author=self.author1).exists())

    def test_delete_by_ordinary_user_not_allowed(self) -> None:
        response = self.client.delete(
            self.article_url,
            headers={
                "Authorization": f"Bearer {AccessToken.for_user(self.ordinary_user)}"
            },
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Article.objects.filter(author=self.author1).exists())
