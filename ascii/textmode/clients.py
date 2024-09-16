from ascii.core.clients import BaseSession


class SixteenColorsClient:
    """
    Slim client for https://16colo.rs/api.php.
    """

    BASE_URL = "https://16colo.rs"
    BASE_API = "https://api.16colo.rs/v1"

    def __init__(self):
        self.session = BaseSession(request_delay=1)

    def get_pack(self, name: str) -> dict:
        resp = self.session.get(
            f"{self.BASE_API}/pack/{name}",
            params={
                "archive": "true",
                "content": "true",
                "groups": "true",
                "artists": "true",
                "fileid": "true",
                "sauce": "true",
            },
        )
        return resp.json()["results"][0]

    def get_year(self, year: int) -> list[dict]:
        resp = self.session.get(
            f"{self.BASE_API}/year/{year}",
            params={"pagesize": 500},
        )
        return resp.json()["results"]

    def get_file(self, path) -> bytes:
        resp = self.session.get(f"{self.BASE_URL}{path}")
        return resp.content
