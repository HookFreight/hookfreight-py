from __future__ import annotations

from typing import Any, Optional


class HookfreightError(Exception):
    """Base error class for all Hookfreight SDK errors."""


class APIError(HookfreightError):
    """Raised when the API returns a non-2xx response."""

    def __init__(self, status: int, body: Any):
        self.status = status
        self.body = body
        self.server_message = None

        if isinstance(body, dict) and "message" in body:
            self.server_message = str(body["message"])

        message = self.server_message or f"API request failed with status {status}"
        super().__init__(message)


class NotFoundError(APIError):
    def __init__(self, body: Any):
        super().__init__(404, body)


class ValidationError(APIError):
    def __init__(self, body: Any):
        super().__init__(400, body)
        if isinstance(body, dict) and isinstance(body.get("errors"), list):
            self.errors = body["errors"]
        else:
            self.errors = []


class AuthenticationError(APIError):
    def __init__(self, body: Any):
        super().__init__(401, body)


class PermissionError(APIError):
    def __init__(self, body: Any):
        super().__init__(403, body)


class ConnectionError(HookfreightError):
    """Raised for timeouts and network-level request failures."""

    def __init__(self, message: str, cause: Optional[BaseException] = None):
        self.cause = cause
        super().__init__(message)
