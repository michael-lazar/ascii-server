import factory
from factory.django import DjangoModelFactory, FileField, ImageField

from ascii.core.tests.factories import UniqueFaker
from ascii.mozz.choices import ArtPostFileType
from ascii.mozz.models import ArtPost


class ArtPostFactory(DjangoModelFactory):
    slug = UniqueFaker("slug")
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text")
    file = FileField()
    file_type = ArtPostFileType.TEXT
    image_x1 = ImageField()

    class Meta:
        model = ArtPost
