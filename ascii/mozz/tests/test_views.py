from django.test import TestCase
from django.urls import reverse

from ascii.mozz.tests.factories import ArtPostFactory, ScrollFileFactory
from ascii.mozz.views import SCROLLFILE_SLUG


class TestMozzScrollFileView(TestCase):
    def test_get(self):
        """Should serve the scrollfile stored in the database as plain text."""
        scrollfile = ScrollFileFactory.create(slug=SCROLLFILE_SLUG, text="hello scroll\n")

        resp = self.client.get(reverse("mozz-scroll-file"))
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/plain"
        assert resp.content.decode("utf-8") == scrollfile.text

    def test_get_missing(self):
        """Should return a 404 when the scrollfile hasn't been uploaded yet."""
        resp = self.client.get(reverse("mozz-scroll-file"))
        assert resp.status_code == 404


class TestMozzIndexView(TestCase):
    def test_get(self):
        """Should render the gallery grid with post titles and dates."""
        post = ArtPostFactory.create(title="Test Piece")

        resp = self.client.get(reverse("mozz-index"))
        assert resp.status_code == 200
        assert b"Test Piece" in resp.content
        assert post.date.strftime("%Y-%m-%d").encode() in resp.content


class TestMozzAboutView(TestCase):
    def test_get(self):
        """Should render the about page with the preamble text."""
        resp = self.client.get(reverse("mozz-about"))
        assert resp.status_code == 200
        assert b"Welcome to my personal ASCII art page!" in resp.content
