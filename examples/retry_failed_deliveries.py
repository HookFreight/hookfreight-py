"""Find and retry failed deliveries from the last 24 hours.

Run: HOOKFREIGHT_API_KEY=hf_sk_... python examples/retry_failed_deliveries.py
"""

import datetime as dt
import os

from hookfreight import Hookfreight

hf = Hookfreight(api_key=os.getenv("HOOKFREIGHT_API_KEY"))


def main() -> None:
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=24)).isoformat()

    deliveries = hf.deliveries.list(
        {
            "status": "failed",
            "start_date": since,
            "limit": 100,
        }
    )["deliveries"]

    print(f"Found {len(deliveries)} failed deliveries since {since}")

    for delivery in deliveries:
        print(f"Retrying {delivery['id']} (event: {delivery['event_id']})")
        hf.deliveries.retry(delivery["id"])

    print("Done.")


if __name__ == "__main__":
    main()
