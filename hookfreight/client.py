from __future__ import annotations

from typing import Optional

from .http import HttpClient, HttpClientConfig
from .resources import Apps, Deliveries, Endpoints, Events

DEFAULT_BASE_URL = "https://api.hookfreight.com/v1"
DEFAULT_TIMEOUT = 30_000


class HookFreight:
    """HookFreight Python SDK client.

    Supports both HookFreight Cloud (with API key) and self-hosted instances
    (with custom base URL).
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        http = HttpClient(
            HttpClientConfig(
                base_url=base_url or DEFAULT_BASE_URL,
                api_key=api_key,
                timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
            )
        )

        self.apps = Apps(http)
        self.endpoints = Endpoints(http)
        self.events = Events(http)
        self.deliveries = Deliveries(http)
