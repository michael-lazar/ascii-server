import os
import re
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from ascii.mozz.choices import ArtPostFileType, ArtPostFontName
from ascii.mozz.models import ArtPost
from ascii.mozz.utils import center_pad_ascii_art


class Command(BaseCommand):
    help = "Import ASCII art from the old static site public directory."

    def add_arguments(self, parser):
        parser.add_argument("public_dir", type=str)

    def handle(self, *args, **options):
        ascii_filename = os.path.join(options["public_dir"], "ascii-art.txt")
        with open(ascii_filename) as fp:
            data = fp.read()

        items = data.split("\n%\n")[1:]
        for item in items:
            lines = item.rstrip().splitlines(keepends=False)
            offset = -2
            date_str, title = lines[offset:]
            title = title.rstrip(".")

            while not date_str.startswith("20"):
                offset -= 1
                title = f"{date_str} {title}"
                date_str = lines[offset]

            slug = re.sub(r"[\W_]+", "-", title.replace("'", "")).lower().strip("-")
            text = center_pad_ascii_art("\n".join(lines[:offset]))

            # image_filename = os.path.join(
            #     options["public_dir"], "ascii-art", date_str, f"{slug}.png"
            # )
            # with open(image_filename, "rb") as fp:
            #     image_raw = fp.read()

            post, created = ArtPost.objects.update_or_create(
                slug=slug,
                date=datetime.strptime(date_str, "%Y-%m-%d").date(),
                defaults={
                    "title": title,
                    "file_type": ArtPostFileType.TEXT,
                    "font_name": ArtPostFontName.MENLO,
                    "file": ContentFile(text, f"{slug}.txt"),
                    # "image_x1": ContentFile(image_raw, f"{slug}.png"),
                },
            )
            self.stdout.write(f"({post}, {created})")
