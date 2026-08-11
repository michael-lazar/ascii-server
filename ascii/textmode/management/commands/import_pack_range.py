from django.core.management.base import BaseCommand

from ascii.textmode.clients import SixteenColorsClient
from ascii.textmode.loaders import SixteenColorsPackImporter


class Command(BaseCommand):
    help = "Import all packs in the given year range from https://16colo.rs"

    def add_arguments(self, parser):
        parser.add_argument("min_year", type=int)
        parser.add_argument("max_year", type=int)
        parser.add_argument("--skip-tags", action="store_true", default=False)
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            default=False,
            help="Skip packs that already exist, instead of re-syncing their metadata",
        )

    def handle(self, *args, **options):
        client = SixteenColorsClient()
        for year in range(options["min_year"], options["max_year"] + 1):
            data = client.get_year(year)

            imported, skipped = 0, 0
            for pack_data in data:
                importer = SixteenColorsPackImporter(
                    pack_data["name"],
                    skip_tags=options["skip_tags"],
                    skip_existing=options["skip_existing"],
                )
                if importer.process() is None:
                    skipped += 1
                else:
                    imported += 1

            self.stdout.write(f"{year}: {imported} packs imported, {skipped} skipped")

        self.stdout.write("Import finished")
