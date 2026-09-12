from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ascii.core.tests.utils import APITestCase
from ascii.mozz.choices import ArtPostFileType
from ascii.mozz.models import ArtPost, ArtPostAttachment, ScrollFile
from ascii.mozz.tests.factories import (
    ArtPostAttachmentFactory,
    ArtPostFactory,
    ScrollFileFactory,
)


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

    def test_detail_attachments(self):
        """Should include attachment download URLs in the response."""
        attachment = ArtPostAttachmentFactory.create(name="reference")

        resp = self.auth_client.get(
            reverse("api:mozz-art-post-detail", args=[attachment.post.slug])
        )
        assert resp.status_code == 200
        assert resp.data["attachments"][0]["name"] == "reference"
        assert resp.data["attachments"][0]["file"]

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


class TestMozzArtPostAttachmentViewSet(APITestCase):
    def test_create(self):
        """Should be able to attach a file to an art post by slug."""
        art_post = ArtPostFactory.create()
        file = SimpleUploadedFile("reference.jpg", b"image content")

        resp = self.auth_client.post(
            reverse("api:mozz-art-post-attachment-list"),
            data={
                "post": art_post.slug,
                "name": "Reference #1",
                "file": file,
            },
            format="multipart",
        )
        assert resp.status_code == 201

        attachment = ArtPostAttachment.objects.get(pk=resp.data["id"])
        assert attachment.post == art_post
        assert attachment.name == "Reference #1"

    def test_create_invalid_post(self):
        """Should reject attachments that reference a missing art post."""
        file = SimpleUploadedFile("reference.jpg", b"image content")

        resp = self.auth_client.post(
            reverse("api:mozz-art-post-attachment-list"),
            data={
                "post": "does-not-exist",
                "name": "Reference #1",
                "file": file,
            },
            format="multipart",
        )
        assert resp.status_code == 400

    def test_delete(self):
        """Should be able to delete an attachment."""
        attachment = ArtPostAttachmentFactory.create()

        resp = self.auth_client.delete(
            reverse("api:mozz-art-post-attachment-detail", args=[attachment.pk])
        )
        assert resp.status_code == 204

        assert not ArtPostAttachment.objects.filter(pk=attachment.pk).exists()


class TestMozzScrollFileViewSet(APITestCase):
    def test_detail(self):
        """Should be able to retrieve a scroll file by slug."""
        scrollfile = ScrollFileFactory.create()

        resp = self.auth_client.get(reverse("api:mozz-scroll-file-detail", args=[scrollfile.slug]))
        assert resp.status_code == 200
        assert resp.data["text"] == scrollfile.text

    def test_create(self):
        """Should be able to create a new scroll file."""
        resp = self.auth_client.post(
            reverse("api:mozz-scroll-file-list"),
            data={"slug": "scrollfile", "text": "art goes here"},
        )
        assert resp.status_code == 201

        assert ScrollFile.objects.filter(slug="scrollfile").exists()

    def test_update(self):
        """Should be able to replace the text of a scroll file."""
        scrollfile = ScrollFileFactory.create()

        resp = self.auth_client.patch(
            reverse("api:mozz-scroll-file-detail", args=[scrollfile.slug]),
            data={"text": "updated text"},
        )
        assert resp.status_code == 200

        scrollfile.refresh_from_db()
        assert scrollfile.text == "updated text"
