from django.core.management.base import BaseCommand

from ascii.textmode.clients import SixteenColorsClient
from ascii.textmode.loaders import SixteenColorsPackImporter


class Command(BaseCommand):
    help = "Import all packs for the given year from https://16colo.rs"

    def add_arguments(self, parser):
        parser.add_argument("year", type=int, help="The year")

    def handle(self, *args, **options):
        self.stdout.write(f"Fetching packs for year {options['year']}")

        client = SixteenColorsClient()
        data = client.get_year(options["year"])
        self.stdout.write(f"Found {len(data)} packs")
        for pack_data in data:
            self.stdout.write(f"Fetching pack {pack_data['name']}")
            importer = SixteenColorsPackImporter(pack_data["name"])
            importer.process()

        self.stdout.write("Import finished")
