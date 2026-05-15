from logging import getLogger

from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.news.models import Article, Tag
from apps.races.models import Series
from tests.config import (
    IMAGE_PATH,
    LARGE_PHOTO,
    TEST_LOGGER_NAME,
)
from tests.utils import (
    get_simple_upload_file,
    get_user,
)

logger = getLogger(TEST_LOGGER_NAME)


class TestArticleUpdate(TestCase):
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
        self.api_client = APIClient()

        self.article = Article.objects.create(
            name="Title",
            author=self.author1,
            content="a" * 255,
            is_published=True,
            cover_image=get_simple_upload_file(IMAGE_PATH),
        )
        self.article.series.add(self.series_f1)
        self.article.tags.add(self.tag_race)

        self.article_url = reverse(
            "articles-detail", kwargs={"slug": self.article.slug}
        )

        self.valid_data = {
            "name": "Updated title",
            "content": "b" * 255,
            "series": [self.series_nascar.id],
            "tags": [self.tag_qualifying.id],
            "is_published": False,
            "cover_image": get_simple_upload_file(IMAGE_PATH),
        }

    def test_success_update(self) -> None:
        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 200)

        self.article.refresh_from_db()

        self.assertEqual(self.article.name, self.valid_data["name"])
        self.assertEqual(self.article.content, self.valid_data["content"])
        self.assertFalse(self.article.is_published)

        self.assertEqual(self.article.series.count(), 1)
        self.assertEqual(self.article.series.first().id, self.series_nascar.id)

        self.assertEqual(self.article.tags.count(), 1)
        self.assertEqual(self.article.tags.first().id, self.tag_qualifying.id)

    def test_update_by_unauthorized_user(self) -> None:
        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 401)

    def test_update_by_not_author(self) -> None:
        token = AccessToken.for_user(self.ordinary_user)
        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": (f"Bearer {token}")},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 403)

    def test_update_another_author_article_not_allowed(self) -> None:
        logger.debug(
            "%s: author1.id=%s, author2.id=%s",
            self._testMethodName,
            self.author1.id,
            self.author2.id,
        )
        token = AccessToken.for_user(self.author2)
        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {token}"},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 403)

    def test_update_nonexistent_article(self) -> None:
        article_url = reverse("articles-detail", kwargs={"slug": "nonexistent-slug"})

        response = self.api_client.patch(
            article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 404)

    def test_update_with_name_length_less_than_min(self) -> None:
        self.valid_data["name"] = "a" * 4

        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Ensure this field has at least 5 characters.",
            str(response.json()["name"]),
        )

    def test_update_with_name_length_more_than_max(self) -> None:
        self.valid_data["name"] = "a" * 256

        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Ensure this field has no more than 255 characters.",
            str(response.json()["name"]),
        )

    def test_update_with_content_length_less_than_min(self) -> None:
        self.valid_data["content"] = "a" * 199

        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Ensure this value has at least 200 characters",
            str(response.json()["content"]),
        )

    def test_update_with_content_length_more_than_max(self) -> None:
        self.valid_data["content"] = "a" * 7501

        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Ensure this value has at most 7500 characters",
            str(response.json()["content"]),
        )

    def test_update_with_nonexistent_series(self) -> None:
        self.valid_data["series"] = [999]

        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn("object does not exist.", str(response.json()["series"]))

    def test_update_with_nonexistent_tag(self) -> None:
        self.valid_data["tags"] = [999]

        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn("object does not exist.", str(response.json()["tags"]))

    def test_update_with_large_cover(self) -> None:
        self.valid_data["cover_image"] = get_simple_upload_file(LARGE_PHOTO)
        response = self.api_client.patch(
            self.article_url,
            data=self.valid_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Max image size is", str(response.json()["cover_image"]))
