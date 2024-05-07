import os
import subprocess
from tempfile import TemporaryDirectory

from django.conf import settings
from django.core.management.base import BaseCommand

from ascii.fudan.models import Document
from ascii.fudan.utils import screenshot_page


class Command(BaseCommand):
    help = "Generate videos from the fudan BBS animation section"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="/groups/rec.faq/ANSI/4/DA7ABCA66/",
        )
        parser.add_argument(
            "--root-url",
            type=str,
            default="http://localhost:8000",
        )
        parser.add_argument(
            "--fps",
            type=int,
            default=7,
        )
        parser.add_argument(
            "--font-size",
            type=int,
            default=24,
            help="Font size in pixels",
        )
        parser.add_argument(
            "--output-dir",
            type=str,
            default=os.path.join(settings.DATA_ROOT, "movies"),
            help="Directory to save generated .mp4 files",
        )

    def handle(self, *args, **options):
        qs = Document.objects.filter(path__startswith=options["path"])
        count = qs.count()

        for i, document in enumerate(qs, start=1):
            self.stdout.write(f"({i}/{count}) Capturing {document}")

            output_filename = os.path.join(options["output_dir"], document.path[1:]) + ".mp4"
            if os.path.exists(output_filename):
                continue

            os.makedirs(os.path.dirname(output_filename), exist_ok=True)

            document_url = f"{options['root_url']}{document.public_url}?plain=1"
            with TemporaryDirectory() as screenshot_dir:
                generator = screenshot_page(
                    document_url,
                    output_dir=screenshot_dir,
                    font_size=options["font_size"],
                )
                for filename in generator:
                    self.stdout.write(self.style.SUCCESS(f"Saved {filename}"))

                command = [
                    "ffmpeg",
                    "-y",
                    "-framerate",
                    f"{options['fps']}",
                    "-pattern_type",
                    "glob",
                    "-i",
                    f"{screenshot_dir}/*.png",
                    "-c:v",
                    "libx264",
                    "-vf",
                    "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    "-pix_fmt",
                    "yuv420p",
                    output_filename,
                ]
                subprocess.run(command)
