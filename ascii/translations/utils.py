from ascii.fudan.ansi import ANSIParser
from ascii.translations.choices import TranslationLanguages
from ascii.translations.models import Translation


def translate_bbs_text(text: str, source: TranslationLanguages) -> str:
    parser = ANSIParser(text)
    original = parser.to_stripped_text()

    translation, created = Translation.objects.get_or_create(original=original, language=source)
    if created:
        translation.populate_translation()

    translated_text = parser.apply_line_indents(translation.translated)
    return translated_text
