from django.core.management.base import BaseCommand

from ascii.textmode.models import ArtFile, ArtFileTag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Refreshing ArtFileTag.artfile_count ...")
        for tag in ArtFileTag.objects.all():
            tag.artfile_count = tag.artfiles.count()
            tag.save(update_fields=["artfile_count"])

        self.stdout.write("Refreshing ArtFile.is_joint ...")
        for artfile in ArtFile.objects.all():
            artfile.is_joint = artfile.tags.artists().count() > 1
            artfile.save(update_fields=["is_joint"])
