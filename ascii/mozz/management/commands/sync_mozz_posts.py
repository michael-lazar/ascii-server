import datetime
import os
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from ascii.mozz.models import ArtPost


class Command(BaseCommand):
    help = "Import art posts from a remote ascii-server instance via the API."

    def add_arguments(self, parser):
        parser.add_argument("--base-url", default=os.environ.get("ASCII_SERVER_BASE_URL"))
        parser.add_argument("--token", default=os.environ.get("ASCII_SERVER_API_TOKEN"))

    def handle(self, *args, **options):
        if not options["base_url"] or not options["token"]:
            raise CommandError("--base-url and --token (or ASCII_SERVER_* env vars) are required")

        session = requests.Session()
        session.headers["Authorization"] = f"Bearer {options['token']}"
        # The public site (unlike /api/) rejects the python-requests user agent
        session.headers["User-Agent"] = "curl/8"

        url = f"{options['base_url']}/api/v1/mozz-art-posts/"
        while url:
            resp = session.get(url)
            resp.raise_for_status()
            data = resp.json()
            for item in data["results"]:
                self.sync_post(session, item)
            url = data["next"]

    def sync_post(self, session: requests.Session, item: dict) -> None:
        if ArtPost.objects.filter(slug=item["slug"]).exists():
            self.stdout.write(f"Skipping {item['slug']} (exists)")
            return

        post = ArtPost(
            slug=item["slug"],
            date=datetime.date.fromisoformat(item["date"]),
            title=item["title"],
            description=item["description"],
            visible=item["visible"],
            favorite=item["favorite"],
            file_type=item["file_type"],
            font_name=item["font_name"],
        )
        post.file = self.download(session, item["file"])
        if item["image_x1"]:
            post.image_x1 = self.download(session, item["image_x1"])

        post.save()
        self.stdout.write(f"Imported {post.slug}")

    def download(self, session: requests.Session, url: str) -> ContentFile:
        resp = session.get(url)
        resp.raise_for_status()
        filename = os.path.basename(urlparse(url).path)
        return ContentFile(resp.content, filename)
