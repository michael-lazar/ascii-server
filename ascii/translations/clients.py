from googletrans import Translator

from ascii.translations.choices import TranslationLanguages


class GoogleTranslateClient:

    def __init__(self):
        self.translator = Translator()

    def translate(self, text: str, language: TranslationLanguages) -> str:
        if text.isspace():
            return text

        try:
            translated = self.translator.translate(text, src=language).text
        except TypeError:
            # The client is buggy, this is raised when the API fails to
            # translate the string for whatever reason.
            #   ``TypeError: 'NoneType' object is not iterable``
            translated = text

        return translated
