from ascii.fudan.ansi import ANSIParser
from ascii.translations.choices import TranslationLanguages
from ascii.translations.models import Translation


def translate_bbs_text(text: str, source: TranslationLanguages) -> str:
    parser = ANSIParser(text)
    text = parser.to_plaintext()

    try:
        translation = Translation.objects.get(original=text, language=source)
    except Translation.objects.DoesNotExist:
        translation = Translation.objects.create(original=text, language=source)
        translation.populate_translation()
        translation.save()

    translated_text = translation.translated
    translated_text = parser.apply_line_offsets(translated_text)
    return translated_text
