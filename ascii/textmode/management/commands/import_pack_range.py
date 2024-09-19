from django.core.management.base import BaseCommand

from ascii.textmode.clients import SixteenColorsClient
from ascii.textmode.loaders import SixteenColorsPackImporter


class Command(BaseCommand):
    help = "Import all packs in the given year range from https://16colo.rs"

    def add_arguments(self, parser):
        parser.add_argument("min_year", type=int)
        parser.add_argument("max_year", type=int)
        parser.add_argument("--skip-tags", action="store_true", default=False)

    def handle(self, *args, **options):
        for year in range(options["min_year"], options["max_year"] + 1):
            self.stdout.write(f"Fetching packs for year {year}")

            client = SixteenColorsClient()
            data = client.get_year(year)
            self.stdout.write(f"Found {len(data)} packs")
            for pack_data in data:
                self.stdout.write(f"Fetching pack {pack_data['name']}")
                importer = SixteenColorsPackImporter(pack_data["name"], options["skip_tags"])
                importer.process()

        self.stdout.write("Import finished")
