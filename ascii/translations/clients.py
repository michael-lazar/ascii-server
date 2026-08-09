from concurrent.futures import ThreadPoolExecutor

import requests
from urllib3.util.retry import Retry


class GoogleTranslateClient:
    """
    Translates text using the free Google Translate web endpoint (the same
    "gtx" API used by Chrome's translate feature).

    Requests are made with plain blocking sockets so the client behaves the
    same under gevent-patched gunicorn workers as it does everywhere else.
    """

    api_url = "https://translate.googleapis.com/translate_a/single"

    def __init__(self, pool_size: int = 20, timeout: float = 10):
        self.pool_size = pool_size
        self.timeout = timeout

    def translate(self, text: str, language: str) -> str:
        """Translates text from the specified language to English."""
        if not text.strip():
            return text

        lines = text.split("\n")

        # The API mangles the line structure of multi-line input (blank lines
        # are dropped and adjacent short lines get merged), but downstream
        # rendering pairs translated lines 1:1 with source lines. Translate
        # line-by-line so the structure never leaves the process.
        unique = list(dict.fromkeys(line for line in lines if line.strip()))

        with requests.Session() as session, ThreadPoolExecutor(self.pool_size) as pool:
            # Retry transient connection drops and rate-limit responses with
            # exponential backoff (0.5s, 1s, 2s), honoring Retry-After on 429.
            retry = Retry(
                total=3,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            # Size the HTTP connection pool to match the thread pool, so
            # threads aren't blocked waiting for a free connection.
            adapter = requests.adapters.HTTPAdapter(
                pool_maxsize=self.pool_size,
                max_retries=retry,
            )
            session.mount("https://", adapter)
            results = pool.map(lambda line: self.translate_line(session, line, language), unique)
            translated = dict(zip(unique, results, strict=True))

        return "\n".join(translated.get(line, line) for line in lines)

    def translate_line(self, session: requests.Session, line: str, language: str) -> str:
        params = {
            "client": "gtx",
            "sl": language,
            "tl": "en",
            "dt": "t",
            "ie": "UTF-8",
            "oe": "UTF-8",
            "q": line,
        }
        response = session.get(self.api_url, params=params, timeout=self.timeout)
        response.raise_for_status()

        # The response is a bare JSON array; index 0 holds the translated
        # sentence segments as [translated, original, ...] pairs.
        segments = response.json()[0] or []
        translated = "".join(segment[0] for segment in segments if segment[0])
        return translated.replace("\n", " ")
