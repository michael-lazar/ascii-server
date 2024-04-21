from ascii.fudan.ansi import ANSIParser
from ascii.translations.choices import TranslationLanguages
from ascii.translations.models import Translation


def translate_bbs_text(text: str, source: TranslationLanguages) -> str:
    parser = ANSIParser(text)
    plaintext = parser.to_plaintext()

    try:
        translation = Translation.objects.get(original=plaintext, language=source)
    except Translation.DoesNotExist:
        translation = Translation.objects.create(original=plaintext, language=source)
        translation.populate_translation()

    translated_text = translation.translated
    translated_text = parser.apply_line_offsets(translated_text)
    return translated_text
