import glob
import os

from django.conf import settings
from django.core.management.base import BaseCommand

DATA_PATH = os.path.join(settings.DATA_ROOT, "spiders", "fundan")


class Command(BaseCommand):
    help = "Import fundan crawl data into the database"

    def handle(self, *args, **options):
        pattern = os.path.join(DATA_PATH, "**", "*.xml")
        for filename in glob.glob(pattern, recursive=True):
            print(filename)
