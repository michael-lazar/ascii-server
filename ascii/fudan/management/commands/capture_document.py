import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ascii.fudan.utils import screenshot_page


class Command(BaseCommand):
    help = "Captures screenshots of a specified webpage"

    def add_arguments(self, parser):
        parser.add_argument(
            "url",
            type=str,
            help="The URL of the webpage to capture",
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
            default=os.path.join(settings.DATA_ROOT, "screenshots"),
            help="Directory to save the screenshots",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the screenshot capture process"))

        generator = screenshot_page(
            url=options["url"],
            output_dir=options["output_dir"],
            font_size=options["font_size"],
        )
        for filename in generator:
            self.stdout.write(self.style.SUCCESS(f"Saved {filename}"))
