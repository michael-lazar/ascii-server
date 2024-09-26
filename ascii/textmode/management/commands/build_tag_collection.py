from django.core.management.base import BaseCommand

from ascii.textmode.models import ArtCollection, ArtFileTag


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="The name of the collection")
        parser.add_argument("tags", nargs="*")

    def handle(self, *args, **options):
        collection, _ = ArtCollection.objects.get_or_create(name=options["name"])

        for item in options["tags"]:
            self.stdout.write(f"Adding artfiles with tag {item}")
            category, name = item.split(":")
            tag = ArtFileTag.objects.get(category=category, name=name)
            for artfile in tag.artfiles.all():
                collection.artfiles.add(artfile)
