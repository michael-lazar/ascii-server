import factory


class UniqueFaker(factory.Faker):
    @classmethod
    def _get_faker(cls, locale=None):
        return super()._get_faker(locale=locale).unique
