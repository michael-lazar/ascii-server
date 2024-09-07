import logging
import time

import requests
from requests.adapters import HTTPAdapter, Retry

_logger = logging.getLogger(__name__)


class BaseSession(requests.Session):
    def __init__(
        self,
        request_delay: float | None = None,
        default_params: dict | None = None,
        retry: Retry | None = None,
        timeout: float = 10,
    ):
        super().__init__()
        self.request_delay = request_delay
        self.default_params = default_params or {}

        self.timeout = timeout
        self.last_request_timestamp: float = 0

        if retry is None:
            retry = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 501, 502, 503, 504],
                raise_on_status=False,
                allowed_methods=["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE"],
            )

        adapter = HTTPAdapter(max_retries=retry)
        self.mount("http://", adapter)
        self.mount("https://", adapter)

    def apply_rate_limit(self) -> None:
        now = time.time()
        if self.request_delay is not None:
            elapsed_time = now - self.last_request_timestamp
            wait_time = self.request_delay - elapsed_time
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_request_timestamp = time.time()

    def request(self, *args, **kwargs) -> requests.Response:
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = self.timeout

        if kwargs.get("params") is None:
            kwargs["params"] = {}
        kwargs["params"] = self.default_params | kwargs["params"]

        self.apply_rate_limit()
        response = super().request(*args, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            _logger.warning(f"HTTP Response Body: {e.response.text}")
            raise

        return response

    def send(self, request: requests.PreparedRequest, **kwargs) -> requests.Response:
        _logger.info(f"Client Request: {request.method} {request.url}")
        return super().send(request, **kwargs)
