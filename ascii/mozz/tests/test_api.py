from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ascii.core.tests.utils import APITestCase
from ascii.mozz.choices import ArtPostFileType
from ascii.mozz.models import ArtPost
from ascii.mozz.tests.factories import ArtPostFactory


class TestMozzArtPostViewSet(APITestCase):
    def test_list(self):
        """Should be able to list art posts."""
        ArtPostFactory.create()

        resp = self.auth_client.get(reverse("api:mozz-art-post-list"))
        assert resp.status_code == 200
        assert resp.data["results"]

    def test_detail(self):
        """Should be able to retrieve a single art post."""
        art_post = ArtPostFactory.create()

        resp = self.auth_client.get(reverse("api:mozz-art-post-detail", args=[art_post.slug]))
        assert resp.status_code == 200
        assert resp.data

    def test_create(self):
        """Should be able to create a new art post."""
        file = SimpleUploadedFile("test.txt", b"test content")

        resp = self.auth_client.post(
            reverse("api:mozz-art-post-list"),
            data={
                "slug": "test-post",
                "title": "Test Post",
                "file": file,
                "file_type": ArtPostFileType.TEXT,
            },
            format="multipart",
        )
        assert resp.status_code == 201

        assert ArtPost.objects.filter(slug="test-post").exists()

    def test_update(self):
        """Should be able to update an existing art post."""
        art_post = ArtPostFactory.create()

        resp = self.auth_client.patch(
            reverse("api:mozz-art-post-detail", args=[art_post.slug]),
            data={"title": "Foobar"},
        )
        assert resp.status_code == 200

        art_post.refresh_from_db()
        assert art_post.title == "Foobar"

    def test_delete(self):
        """Should be able to delete an art post."""
        art_post = ArtPostFactory.create()

        resp = self.auth_client.delete(reverse("api:mozz-art-post-detail", args=[art_post.slug]))
        assert resp.status_code == 204

        assert not ArtPost.objects.filter(pk=art_post.pk).exists()
