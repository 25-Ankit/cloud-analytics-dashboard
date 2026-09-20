import argparse
import os
import time
from datetime import datetime, timezone

from stream.stream import get_connection, get_checkpoint, get_events_after, init_db, set_checkpoint

DEFAULT_BATCH_SIZE = 500


def process_once(batch_size: int = DEFAULT_BATCH_SIZE) -> int:
    init_db()
    checkpoint = get_checkpoint()
    events = get_events_after(checkpoint, batch_size)
    if not events:
        return 0

    with get_connection() as conn:
        for event in events:
            conn.execute(
                """
                INSERT INTO analytics_totals(id, total_orders, total_sales, updated_at)
                VALUES (1, 1, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    total_orders = total_orders + 1,
                    total_sales = total_sales + excluded.total_sales,
                    updated_at = excluded.updated_at
                """,
                (float(event["amount"]), datetime.now(timezone.utc).isoformat()),
            )

            conn.execute(
                """
                INSERT INTO city_sales(city, orders, sales)
                VALUES (?, 1, ?)
                ON CONFLICT(city) DO UPDATE SET
                    orders = orders + 1,
                    sales = sales + excluded.sales
                """,
                (event["city"], float(event["amount"])),
            )

            conn.execute(
                """
                INSERT INTO category_sales(category, orders, sales)
                VALUES (?, 1, ?)
                ON CONFLICT(category) DO UPDATE SET
                    orders = orders + 1,
                    sales = sales + excluded.sales
                """,
                (event["category"], float(event["amount"])),
            )

        set_checkpoint(events[-1]["id"])

    return len(events)


def run_loop(interval: float, batch_size: int) -> None:
    while True:
        processed = process_once(batch_size)
        if processed:
            print(f"processed={processed}", flush=True)
        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Incremental analytics processor")
    parser.add_argument("--once", action="store_true", help="Process one batch and exit")
    parser.add_argument("--interval", type=float, default=float(os.getenv("PROCESSOR_INTERVAL", "2")))
    parser.add_argument("--batch-size", type=int, default=int(os.getenv("PROCESSOR_BATCH_SIZE", DEFAULT_BATCH_SIZE)))
    args = parser.parse_args()

    if args.once:
        print(f"processed={process_once(args.batch_size)}")
    else:
        init_db()
        run_loop(args.interval, args.batch_size)
