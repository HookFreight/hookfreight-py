from __future__ import annotations

from typing import Optional

from ..http import HttpClient
from ..pagination import MAX_LIMIT, clamp_pagination
from ..types import (
    CreateEndpointParams,
    Endpoint,
    EndpointListResponse,
    PaginationParams,
    UpdateEndpointParams,
)
from ._common import as_dict, unwrap_data


class Endpoints:
    def __init__(self, http: HttpClient):
        self._http = http

    def list(self, app_id: str, params: Optional[PaginationParams] = None) -> EndpointListResponse:
        payload = self._http.get(
            f"/apps/{app_id}/endpoints",
            clamp_pagination(params, MAX_LIMIT["endpoints"]),
        )
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def create(self, params: CreateEndpointParams) -> Endpoint:
        payload = self._http.post("/endpoints", params)
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def get(self, endpoint_id: str) -> Endpoint:
        payload = self._http.get(f"/endpoints/{endpoint_id}")
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def update(self, endpoint_id: str, params: UpdateEndpointParams) -> Endpoint:
        payload = self._http.put(f"/endpoints/{endpoint_id}", params)
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def delete(self, endpoint_id: str) -> Endpoint:
        payload = self._http.delete(f"/endpoints/{endpoint_id}")
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]
