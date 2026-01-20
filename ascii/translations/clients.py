from googletrans import Translator


class GoogleTranslateClient:

    def __init__(self):
        self.translator = Translator()

    def split_text(self, text: str, chunk_size: int = 200):
        lines = text.split("\n")
        for i in range(0, len(lines), chunk_size):
            yield "\n".join(lines[i : i + chunk_size])

    def translate(self, text: str, language: str) -> str:
        """Translates text to the specified language."""
        if text.isspace():
            return text

        translated_segments = []
        for segment in self.split_text(text):
            try:
                translated = self.translator.translate(segment, src=language).text
                translated_segments.append(translated)
            except TypeError:
                # The client is buggy, this is raised when the API fails to
                # translate the string for whatever reason.
                #   ``TypeError: 'NoneType' object is not iterable``
                translated_segments.append(segment)

        return "\n".join(translated_segments)
