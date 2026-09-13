from django.test import TestCase
from django.urls import reverse

from ascii.mozz.tests.factories import ArtPostFactory
from ascii.mozz.views import SCROLLFILE_PATH


class TestMozzScrollFileView(TestCase):
    def test_get(self):
        """Should serve the scrollfile tracked in the git repo as plain text."""
        with open(SCROLLFILE_PATH) as fp:
            text = fp.read()

        resp = self.client.get(reverse("mozz-scroll-file"))
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/plain"
        assert resp.content.decode("utf-8") == text


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
