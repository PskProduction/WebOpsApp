from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Article


class ArticleViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.other_user = get_user_model().objects.create(username="otheruser", password="otherpassword")
        self.client.login(username="testuser", password="testpassword")
        self.article = Article.objects.create(title="test Article", content="Some text", author=self.user)

    def test_article_create_view_authenticated_user(self):
        response = self.client.post(
            reverse("blogapp:article_add"), {"title": "New test Article", "content": "New article text"}
        )
        self.assertEqual(response.status_code, 302)
        new_article = Article.objects.get(title="New test Article")
        self.assertEqual(new_article.content, "New article text")
        self.assertEqual(new_article.author, self.user)

    def test_article_update_view_authenticated_user(self):
        updated_content = "Updated article text"

        response = self.client.post(
            reverse("blogapp:article_update", args=[self.article.pk]),
            {"title": self.article.title, "content": updated_content},
        )

        self.assertEqual(response.status_code, 302)

        updated_article = Article.objects.get(pk=self.article.pk)

        self.assertEqual(updated_article.content, updated_content)
        self.assertEqual(updated_article.author, self.user)

    def test_article_delete_view_authenticated_user(self):
        response = self.client.post(reverse("blogapp:article_delete", args=[self.article.pk]))

        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(pk=self.article.pk)

    def test_article_create_view_unauthenticated_user(self):
        self.client.logout()

        response = self.client.post(
            reverse("blogapp:article_add"), {"title": "New Post", "content": "This is a new post."}
        )
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(title="New Post")

    def test_article_update_view_other_user(self):
        self.client.logout()
        self.client.login(username="otheruser", password="otherpassword")

        updated_content = "Updated article text"

        response = self.client.post(
            reverse("blogapp:article_update", args=[self.article.pk]),
            {"title": self.article.title, "content": updated_content},
        )

        updated_article = Article.objects.get(pk=self.article.pk)
        self.assertEqual(updated_article.content, "Some text")
        self.assertEqual(updated_article.author, self.user)

    def test_article_delete_view_other_user(self):
        self.client.logout()
        self.client.login(username="otheruser", password="otherpassword")

        response = self.client.post(reverse("blogapp:article_delete", args=[self.article.pk]))

        self.assertEqual(Article.objects.get(pk=self.article.pk).content, "Some text")
