# hookfreight

Official Python SDK for **[HookFreight](https://hookfreight.com)**.

Capture, inspect, replay, and reliably deliver webhooks with full visibility.

## Installation

```bash
pip install hookfreight
```

## Quick Start

### HookFreight Cloud

```python
from hookfreight import HookFreight

hf = HookFreight(api_key="hf_sk_...")

result = hf.deliveries.list({"limit": 10})
print(result["deliveries"])
```

### Self-Hosted

```python
from hookfreight import HookFreight

hf = HookFreight(base_url="http://localhost:3030/api/v1")
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | `str` | — | API key for HookFreight Cloud. Optional for self-hosted. |
| `base_url` | `str` | `https://api.hookfreight.com/v1` | Base URL of the API. Override for self-hosted. |
| `timeout` | `int` | `30000` | Request timeout in milliseconds. |

## Usage

```python
from hookfreight import HookFreight

hf = HookFreight(api_key="hf_sk_...")

app = hf.apps.create({"name": "My App"})
endpoint = hf.endpoints.create({
    "name": "Stripe",
    "app_id": app["id"],
    "forward_url": "https://example.com/webhooks/stripe",
})

event = hf.events.get("evt_...")
print(event["body"])

stats = hf.deliveries.queue_stats()
print(stats)
```

## Error Handling

```python
from hookfreight import HookFreight, NotFoundError, ValidationError, ConnectionError

hf = HookFreight(api_key="hf_sk_...")

try:
    hf.apps.get("app_nonexistent")
except NotFoundError:
    print("App not found")
except ValidationError as err:
    print(err.errors)
except ConnectionError as err:
    print(err)
```

## Examples

- `examples/basic_usage.py`
- `examples/manage_endpoints.py`
- `examples/retry_failed_deliveries.py`
- `examples/monitor_queue.py`

Run an example:

```bash
HOOKFREIGHT_API_KEY=hf_sk_... python examples/basic_usage.py
```

## License

Apache-2.0
