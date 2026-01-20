from django.test import TestCase
from django.urls import reverse


class TestIndexView(TestCase):
    def test_get(self):
        response = self.client.get(reverse("index"))
        assert response.status_code == 200
