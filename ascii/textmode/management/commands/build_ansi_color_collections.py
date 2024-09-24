from django.core.management.base import BaseCommand

from ascii.textmode.constants import ANSI_COLORS
from ascii.textmode.models import ArtCollection, ArtFile
from ascii.textmode.sauce import ANSIFileInspector


class Command(BaseCommand):

    def handle(self, *args, **options):
        for artfile in ArtFile.objects.ansi():
            inspector = ANSIFileInspector(artfile)
            try:
                colors = inspector.get_colors()
            except Exception as e:
                self.stderr.write(str(e))
                continue

            # Allow black/white in any color palette
            if 0 in colors:
                colors.remove(0)
            if 7 in colors:
                colors.remove(7)

            # Skip palettes with > 2 colors
            if len(colors) > 2:
                continue

            if not colors:
                name = "Black/White"
                description = "Black and White"
            else:
                name = "/".join(ANSI_COLORS[c] for c in colors)
                description = " and ".join(ANSI_COLORS[c] for c in colors)

            name = name + " ANSi"
            description = description + "ANSi"

            collection, _ = ArtCollection.objects.get_or_create(name=name, description=description)
            collection.artfiles.add(artfile)

            self.stdout.write(name)
