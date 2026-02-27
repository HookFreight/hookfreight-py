"""Programmatically manage endpoints (useful in CI/CD pipelines).

Run: HOOKFREIGHT_API_KEY=hf_sk_... python examples/manage_endpoints.py app_...
"""

import os
import sys

from hookfreight import HookFreight

hf = HookFreight(api_key=os.getenv("HOOKFREIGHT_API_KEY"))


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python examples/manage_endpoints.py <app_id>")
        raise SystemExit(1)

    app_id = sys.argv[1]

    endpoints = hf.endpoints.list(app_id)["endpoints"]
    print(f"App {app_id} has {len(endpoints)} endpoint(s):")

    for endpoint in endpoints:
        print(f"  {endpoint['id']} - {endpoint['name']} (active: {endpoint['is_active']})")

    for endpoint in endpoints:
        hf.endpoints.update(endpoint["id"], {"is_active": False})
        print(f"Paused {endpoint['id']}")

    # ... maintenance window ...

    for endpoint in endpoints:
        hf.endpoints.update(endpoint["id"], {"is_active": True})
        print(f"Resumed {endpoint['id']}")


if __name__ == "__main__":
    main()
