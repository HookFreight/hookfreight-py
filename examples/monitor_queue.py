"""Monitor delivery queue health for alerting.

Run: HOOKFREIGHT_API_KEY=hf_sk_... python examples/monitor_queue.py
"""

import os

from hookfreight import Hookfreight

hf = Hookfreight(api_key=os.getenv("HOOKFREIGHT_API_KEY"))


def main() -> None:
    stats = hf.deliveries.queue_stats()

    print("Queue Stats:")
    print(f"  Waiting:   {stats['waiting']}")
    print(f"  Active:    {stats['active']}")
    print(f"  Completed: {stats['completed']}")
    print(f"  Failed:    {stats['failed']}")
    print(f"  Delayed:   {stats['delayed']}")

    if stats["waiting"] > 100:
        print("WARNING: High queue backlog")

    if stats["failed"] > 10:
        print("WARNING: Multiple failed deliveries")


if __name__ == "__main__":
    main()
