from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict


class PaginationParams(TypedDict, total=False):
    offset: int
    limit: int


class PaginatedResult(TypedDict):
    has_next: bool
    limit: int
    offset: int


class App(TypedDict, total=False):
    id: str
    name: str
    description: str
    createdAt: str
    updatedAt: str


class CreateAppParams(TypedDict, total=False):
    name: str
    description: str


class UpdateAppParams(TypedDict, total=False):
    name: str
    description: str


class AppListResponse(PaginatedResult):
    apps: List[App]


class AppDeleteResponse(TypedDict, total=False):
    app: App
    connected_endpoints: int
    deleted_endpoints: int
    deleted_events: int


class EndpointAuthentication(TypedDict):
    header_name: str
    header_value: str


class Endpoint(TypedDict, total=False):
    id: str
    name: str
    description: str
    app_id: str
    authentication: EndpointAuthentication
    http_timeout: int
    is_active: bool
    rate_limit: int
    rate_limit_duration: int
    forward_url: str
    forwarding_enabled: bool
    hook_token: str
    createdAt: str
    updatedAt: str


class CreateEndpointParams(TypedDict, total=False):
    name: str
    app_id: str
    forward_url: str
    description: str
    authentication: EndpointAuthentication
    http_timeout: int
    is_active: bool
    rate_limit: int
    rate_limit_duration: int
    forwarding_enabled: bool


class UpdateEndpointParams(TypedDict, total=False):
    name: str
    description: str
    authentication: EndpointAuthentication
    http_timeout: int
    is_active: bool
    rate_limit: int
    rate_limit_duration: int
    forward_url: str
    forwarding_enabled: bool


class EndpointListResponse(PaginatedResult):
    endpoints: List[Endpoint]


EventAuthStatus = Literal["passed", "unauthorized", "disabled"]


class WebhookEvent(TypedDict, total=False):
    id: str
    endpoint_id: str
    recieved_at: str
    method: str
    original_url: str
    path: str
    headers: Dict[str, Any]
    source_ip: str
    user_agent: str
    size_bytes: int
    auth_status: EventAuthStatus
    content_type: Optional[str]
    content_encoding: Optional[str]
    body: Any
    createdAt: str
    updatedAt: str


class ListEventsParams(PaginationParams, total=False):
    endpoint_id: str
    method: str
    start_date: str
    end_date: str
    auth_status: EventAuthStatus


class EventListResponse(PaginatedResult):
    events: List[WebhookEvent]


DeliveryStatus = Literal["delivered", "failed", "timeout"]


class Delivery(TypedDict, total=False):
    id: str
    parent_delivery_id: str
    status: DeliveryStatus
    event_id: str
    destination_url: str
    response_status: int
    response_headers: Dict[str, Any]
    response_body: Any
    duration: int
    error_message: str
    createdAt: str
    updatedAt: str


class ListDeliveriesParams(PaginationParams, total=False):
    status: DeliveryStatus
    event_id: str
    start_date: str
    end_date: str


class DeliveryListResponse(PaginatedResult):
    deliveries: List[Delivery]


class QueueStats(TypedDict):
    waiting: int
    active: int
    completed: int
    failed: int
    delayed: int
