from django.templatetags.static import static
from django.test import TestCase
from django.urls import reverse


class TestMozzScrollFileView(TestCase):
    def test_get(self):
        """The historical scrollfile URL should redirect to the static file."""
        resp = self.client.get(reverse("mozz-scroll-file"))
        assert resp.status_code == 302
        assert resp["Location"] == static("mozz/scrollfile.txt")
