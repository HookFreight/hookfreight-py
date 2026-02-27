from __future__ import annotations

from typing import Dict, Optional

from ..http import HttpClient
from ..pagination import MAX_LIMIT, clamp_pagination
from ..types import EventListResponse, ListEventsParams, PaginationParams, WebhookEvent
from ._common import as_dict, unwrap_data


class Events:
    def __init__(self, http: HttpClient):
        self._http = http

    def list(self, params: Optional[ListEventsParams] = None) -> EventListResponse:
        payload = self._http.get("/events", clamp_pagination(params, MAX_LIMIT["events"]))
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def get(self, event_id: str) -> WebhookEvent:
        payload = self._http.get(f"/events/{event_id}")
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def list_by_endpoint(
        self,
        endpoint_id: str,
        params: Optional[PaginationParams] = None,
    ) -> EventListResponse:
        payload = self._http.get(
            f"/endpoints/{endpoint_id}/events",
            clamp_pagination(params, MAX_LIMIT["events"]),
        )
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def replay(self, event_id: str) -> None:
        self._http.post(f"/events/{event_id}/replay")

    # Backward-compatible alias for mixed style call sites.
    def listByEndpoint(
        self,
        endpoint_id: str,
        params: Optional[PaginationParams] = None,
    ) -> EventListResponse:
        return self.list_by_endpoint(endpoint_id, params)
