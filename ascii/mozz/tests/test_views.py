from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class TestMozzScrollFileView(TestCase):
    def test_get(self):
        """Should serve the scrollfile tracked in the git repo as plain text."""
        with open(settings.SCROLLFILE_PATH) as fp:
            text = fp.read()

        resp = self.client.get(reverse("mozz-scroll-file"))
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/plain"
        assert resp.content.decode("utf-8") == text
