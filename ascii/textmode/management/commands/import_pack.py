from django.core.management.base import BaseCommand

from ascii.textmode.loaders import SixteenColorsPackImporter


class Command(BaseCommand):
    help = "Import an art pack from https://16colo.rs"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="The name of the pack")

    def handle(self, *args, **options):
        self.stdout.write(f"Fetching pack {options['name']}")
        importer = SixteenColorsPackImporter(options["name"])
        pack = importer.process()
        self.stdout.write(f"Import finished: {pack}")
