from django.core.management.base import BaseCommand, CommandParser

from ascii.translations.choices import TranslationLanguages
from ascii.translations.utils import translate_bbs_text


class Command(BaseCommand):
    help = "Translate a string."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "text",
            help="Text to translate",
        )
        parser.add_argument(
            "--language",
            choices=TranslationLanguages.values,
            default=TranslationLanguages.CHINESE_SIMPLIFIED,
            help="Source language",
        )

    def handle(self, *args, **options):
        text = translate_bbs_text(options["text"], options["language"])
        self.stdout.write(text)
