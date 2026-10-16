from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user("writer", password="pass12345!")
        cat = Category.objects.create(name="Python")
        cls.live = Post.objects.create(
            title="Hello Django", author=user, category=cat, body="First post.",
            status=Post.Status.PUBLISHED,
        )
        cls.draft = Post.objects.create(title="Secret draft", author=user, body="WIP")
        cls.future = Post.objects.create(
            title="Scheduled", author=user, body="Later",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() + timedelta(days=1),
        )

    def test_slug_generated_and_unique(self):
        dup = Post.objects.create(title="Hello Django", author=self.live.author, body="x")
        self.assertEqual(self.live.slug, "hello-django")
        self.assertEqual(dup.slug, "hello-django-2")

    def test_list_shows_only_published(self):
        resp = self.client.get(reverse("blog:post_list"))
        self.assertContains(resp, "Hello Django")
        self.assertNotContains(resp, "Secret draft")
        self.assertNotContains(resp, "Scheduled")

    def test_draft_detail_404(self):
        resp = self.client.get(reverse("blog:post_detail", args=[self.draft.slug]))
        self.assertEqual(resp.status_code, 404)

    def test_comment_post_redirects(self):
        url = self.live.get_absolute_url()
        resp = self.client.post(url, {"name": "Ali", "body": "Nice!"})
        self.assertRedirects(resp, url)
        self.assertEqual(self.live.comments.count(), 1)

    def test_search(self):
        resp = self.client.get(reverse("blog:post_list"), {"q": "first"})
        self.assertContains(resp, "Hello Django")

    def test_api(self):
        data = self.client.get(reverse("blog:api_posts")).json()
        self.assertEqual([p["slug"] for p in data["results"]], ["hello-django"])
