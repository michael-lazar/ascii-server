from googletrans import Translator

from ascii.translations.choices import TranslationLanguages


class GoogleTranslateClient:

    def __init__(self):
        self.translator = Translator()

    def translate(self, text: str, language: TranslationLanguages) -> str:
        translated = self.translator.translate(text, src=language)
        return translated.text
