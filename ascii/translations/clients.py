import asyncio

from googletrans import Translator


class GoogleTranslateClient:
    def translate(self, text: str, language: str) -> str:
        """Translates text to the specified language."""
        if not text.strip():
            return text

        return asyncio.run(self._translate(text, language))

    async def _translate(self, text: str, language: str) -> str:
        lines = text.split("\n")

        # Downstream rendering pairs translated lines 1:1 with source lines,
        # but Google mangles the line structure of multi-line input (blank
        # lines are dropped and adjacent short lines get merged). Translate
        # line-by-line so the structure never leaves the process.
        unique = list(dict.fromkeys(line for line in lines if line.strip()))

        # googletrans 4.x is async-only, and its Translator must be used as a
        # context manager so the underlying httpx client is closed with the
        # event loop it was created on.
        async with Translator(list_operation_max_concurrency=10) as translator:
            results = await translator.translate(unique, src=language)

        translated = {
            line: result.text.replace("\n", " ")
            for line, result in zip(unique, results, strict=True)
        }
        return "\n".join(translated.get(line, line) for line in lines)
