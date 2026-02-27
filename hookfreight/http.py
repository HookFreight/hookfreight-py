from __future__ import annotations

import json
import socket
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

from .errors import (
    APIError,
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    PermissionError,
    ValidationError,
)

SDK_VERSION = "0.1.0"


@dataclass(frozen=True)
class HttpClientConfig:
    base_url: str
    api_key: Optional[str]
    timeout: int


class HttpClient:
    def __init__(self, config: HttpClientConfig):
        self._base_url = config.base_url.rstrip("/")
        self._api_key = config.api_key
        self._timeout_ms = config.timeout

    def request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[Any] = None,
        query: Optional[Mapping[str, object]] = None,
    ) -> Any:
        url = urljoin(f"{self._base_url}/", path.lstrip("/"))

        if query:
            cleaned_query = {
                key: str(value)
                for key, value in query.items()
                if value is not None
            }
            if cleaned_query:
                url = f"{url}?{urlencode(cleaned_query)}"

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "User-Agent": f"hookfreight-python/{SDK_VERSION}",
        }

        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        payload = None
        if body is not None:
            payload = json.dumps(body).encode("utf-8")

        request = Request(url=url, data=payload, headers=headers, method=method)

        try:
            with urlopen(request, timeout=self._timeout_ms / 1000) as response:
                raw = response.read()
                return self._decode_body(raw, response.headers.get("Content-Type", ""))
        except HTTPError as error:
            raw = error.read()
            parsed = self._decode_body(raw, error.headers.get("Content-Type", ""))
            raise self._build_error(error.code, parsed) from None
        except (TimeoutError, socket.timeout) as error:
            raise ConnectionError(
                f"Request timed out after {self._timeout_ms}ms",
                cause=error,
            ) from error
        except URLError as error:
            raise ConnectionError(str(error.reason), cause=error) from error
        except OSError as error:
            raise ConnectionError(str(error), cause=error) from error

    def get(self, path: str, query: Optional[Mapping[str, object]] = None) -> Any:
        return self.request("GET", path, query=query)

    def post(self, path: str, body: Optional[Any] = None) -> Any:
        return self.request("POST", path, body=body)

    def put(self, path: str, body: Optional[Any] = None) -> Any:
        return self.request("PUT", path, body=body)

    def delete(self, path: str) -> Any:
        return self.request("DELETE", path)

    @staticmethod
    def _decode_body(raw: bytes, content_type: str) -> Any:
        if not raw:
            return {}

        text = raw.decode("utf-8", errors="replace")

        if "application/json" in content_type:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text

        return text

    @staticmethod
    def _build_error(status: int, body: Any) -> APIError:
        if status == 400:
            return ValidationError(body)
        if status == 401:
            return AuthenticationError(body)
        if status == 403:
            return PermissionError(body)
        if status == 404:
            return NotFoundError(body)
        return APIError(status, body)
