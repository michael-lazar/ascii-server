import asyncio

from googletrans import Translator


class GoogleTranslateClient:
    def split_text(self, text: str, chunk_size: int = 200):
        lines = text.split("\n")
        for i in range(0, len(lines), chunk_size):
            yield "\n".join(lines[i : i + chunk_size])

    def translate(self, text: str, language: str) -> str:
        """Translates text to the specified language."""
        if text.isspace():
            return text

        return asyncio.run(self._translate(text, language))

    async def _translate(self, text: str, language: str) -> str:
        # googletrans 4.x is async-only, and its Translator must be used as a
        # context manager so the underlying httpx client is closed with the
        # event loop it was created on.
        async with Translator() as translator:
            translated_segments = []
            for segment in self.split_text(text):
                translated = await translator.translate(segment, src=language)
                translated_segments.append(translated.text)

        return "\n".join(translated_segments)
