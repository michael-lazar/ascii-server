import factory
from factory.django import DjangoModelFactory, FileField

from ascii.core.tests.factories import UniqueFaker
from ascii.textmode.choices import TagCategory
from ascii.textmode.models import ArtFile, ArtFileTag, ArtPack


class ArtPackFactory(DjangoModelFactory):
    name = UniqueFaker("name")
    year = 2024
    zip_file = FileField()

    class Meta:
        model = ArtPack


class ArtFileFactory(DjangoModelFactory):
    name = UniqueFaker("name")
    pack = factory.SubFactory(ArtPackFactory)
    raw_file = FileField()

    class Meta:
        model = ArtFile


class ArtFileTagFactory(DjangoModelFactory):
    name = UniqueFaker("name")
    category = TagCategory.ARTIST

    class Meta:
        model = ArtFileTag
