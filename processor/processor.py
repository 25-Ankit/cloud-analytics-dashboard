import argparse
import os
import time
from datetime import datetime, timezone

from stream.stream import get_connection, get_checkpoint, get_events_after, init_db

DEFAULT_BATCH_SIZE = 500


def process_once(batch_size: int = DEFAULT_BATCH_SIZE) -> int:
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")
    init_db()
    checkpoint = get_checkpoint()
    events = get_events_after(checkpoint, batch_size)
    if not events:
        return 0

    # Aggregate updates AND checkpoint happen in the same SQLite transaction.
    # This avoids the database-lock bug caused by opening a second connection.
    with get_connection() as conn:
        for event in events:
            amount = float(event["amount"])
            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                """INSERT INTO analytics_totals(id,total_orders,total_sales,updated_at)
                VALUES(1,1,?,?) ON CONFLICT(id) DO UPDATE SET
                total_orders=total_orders+1,total_sales=total_sales+excluded.total_sales,updated_at=excluded.updated_at""",
                (amount, now),
            )
            conn.execute(
                """INSERT INTO city_sales(city,orders,sales) VALUES(?,1,?)
                ON CONFLICT(city) DO UPDATE SET orders=orders+1,sales=sales+excluded.sales""",
                (event["city"], amount),
            )
            conn.execute(
                """INSERT INTO category_sales(category,orders,sales) VALUES(?,1,?)
                ON CONFLICT(category) DO UPDATE SET orders=orders+1,sales=sales+excluded.sales""",
                (event["category"], amount),
            )
        conn.execute("UPDATE processor_state SET last_event_id=? WHERE id=1", (int(events[-1]["id"]),))
    return len(events)


def run_loop(interval: float, batch_size: int) -> None:
    while True:
        count = process_once(batch_size)
        if count:
            print(f"processed={count}", flush=True)
        time.sleep(interval)


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--once", action="store_true")
    p.add_argument("--interval", type=float, default=float(os.getenv("PROCESSOR_INTERVAL","2")))
    p.add_argument("--batch-size", type=int, default=int(os.getenv("PROCESSOR_BATCH_SIZE",DEFAULT_BATCH_SIZE)))
    a=p.parse_args()
    if a.once:
        print(f"processed={process_once(a.batch_size)}")
    else:
        init_db(); run_loop(a.interval,a.batch_size)
