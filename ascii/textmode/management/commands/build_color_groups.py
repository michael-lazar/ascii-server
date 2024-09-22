from django.core.management.base import BaseCommand

from ascii.textmode.models import ArtFile, Gallery
from ascii.textmode.sauce import ANSI_COLORS, ANSIFileInspector


class Command(BaseCommand):

    def handle(self, *args, **options):
        for artfile in ArtFile.objects.ansi():
            inspector = ANSIFileInspector(artfile)
            try:
                colors = inspector.get_colors()
            except Exception as e:
                self.stderr.write(str(e))
                continue

            name = f"Color Palette: {colors}"

            description = "\n".join(
                (
                    ", ".join(ANSI_COLORS[c] for c in colors if c < 8),
                    ", ".join(ANSI_COLORS[c] for c in colors if 8 <= c),
                )
            )

            gallery, _ = Gallery.objects.get_or_create(name=name, description=description)
            gallery.artfiles.add(artfile)

            self.stdout.write(name)
