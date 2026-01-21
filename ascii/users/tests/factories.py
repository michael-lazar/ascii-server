import factory
from django.contrib.auth.models import User
from factory import Faker
from factory.django import DjangoModelFactory

from ascii.core.tests.factories import UniqueFaker
from ascii.users.models import AuthToken


def populate_password_fn(obj: User, *args, **kwargs) -> None:
    obj.set_unusable_password()
    obj.save()


class UserFactory(DjangoModelFactory):
    username = UniqueFaker("user_name")
    email = UniqueFaker("email")
    password = factory.PostGeneration(populate_password_fn)
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    class Meta:
        model = User
        django_get_or_create = ["username"]
        skip_postgeneration_save = True


class AuthTokenFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = AuthToken
