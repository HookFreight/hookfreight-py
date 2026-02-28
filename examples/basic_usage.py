"""Basic usage of the Hookfreight Python SDK.

Run: HOOKFREIGHT_API_KEY=hf_sk_... python examples/basic_usage.py
"""

import osHookfreight

from Hookfreight import Hookfreight

hf = Hookfreight(
    api_key=os.getenv("HOOKFREIGHT_API_KEY"),
    # base_url="http://localhost:3030/api/v1",  # for self-hosted
)


def main() -> None:
    apps = hf.apps.list()["apps"]
    print("Apps:", apps)

    app = hf.apps.create({"name": "My App", "description": "Created via SDK"})
    print("Created app:", app["id"])

    endpoint = hf.endpoints.create(
        {
            "name": "Stripe Webhooks",
            "app_id": app["id"],
            "forward_url": "https://example.com/webhooks/stripe",
        }
    )
    print("Created endpoint:", endpoint["id"])
    print("Webhook URL:", f"https://api.hookfreight.com/{endpoint['hook_token']}")

    events = hf.events.list({"limit": 10})["events"]
    print(f"Found {len(events)} events")

    deliveries = hf.deliveries.list({"limit": 10})["deliveries"]
    print(f"Found {len(deliveries)} deliveries")

    hf.endpoints.delete(endpoint["id"])
    hf.apps.delete(app["id"])
    print("Cleaned up.")


if __name__ == "__main__":
    main()
