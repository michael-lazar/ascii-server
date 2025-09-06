from datetime import datetime

from django.core.management.base import BaseCommand

from ascii.textmode.clients import SixteenColorsClient
from ascii.textmode.loaders import SixteenColorsPackImporter


class Command(BaseCommand):
    help = "Import all new packs from https://16colo.rs"

    def handle(self, *args, **options):
        now = datetime.now()

        client = SixteenColorsClient()
        data = client.get_year(now.year)
        for pack_data in data:
            importer = SixteenColorsPackImporter(
                pack_data["name"],
                skip_tags=False,
                skip_existing=True,
            )
            importer.process()

        self.stdout.write("Import finished")
