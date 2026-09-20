import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

DEFAULT_DB_PATH = "data/events.db"


def get_db_path() -> str:
    return os.getenv("ANALYTICS_DB_PATH", DEFAULT_DB_PATH)


def _ensure_parent(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection():
    path = get_db_path()
    _ensure_parent(path)
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA foreign_keys=ON")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL DEFAULT 'sale',
            city TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount >= 0),
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS processor_state (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            last_event_id INTEGER NOT NULL DEFAULT 0
        );

        INSERT OR IGNORE INTO processor_state(id, last_event_id)
        VALUES (1, 0);

        CREATE TABLE IF NOT EXISTS analytics_totals (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            total_orders INTEGER NOT NULL DEFAULT 0,
            total_sales REAL NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL
        );

        INSERT OR IGNORE INTO analytics_totals(id, total_orders, total_sales, updated_at)
        VALUES (1, 0, 0, CURRENT_TIMESTAMP);

        CREATE TABLE IF NOT EXISTS city_sales (
            city TEXT PRIMARY KEY,
            orders INTEGER NOT NULL DEFAULT 0,
            sales REAL NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS category_sales (
            category TEXT PRIMARY KEY,
            orders INTEGER NOT NULL DEFAULT 0,
            sales REAL NOT NULL DEFAULT 0
        );

        CREATE INDEX IF NOT EXISTS idx_events_id ON events(id);
        CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at);
        """)


def _validate_event(event: Dict[str, Any]) -> None:
    for field in ("city", "category", "amount"):
        if field not in event:
            raise ValueError(f"missing field: {field}")
    if not str(event["city"]).strip():
        raise ValueError("city must not be empty")
    if not str(event["category"]).strip():
        raise ValueError("category must not be empty")
    try:
        amount = float(event["amount"])
    except (TypeError, ValueError):
        raise ValueError("amount must be numeric")
    if amount < 0:
        raise ValueError("amount must be >= 0")


def put_event(
    city: str,
    category: str,
    amount: float,
    event_type: str = "sale",
    created_at: str | None = None,
) -> int:
    event = {
        "city": city,
        "category": category,
        "amount": amount,
        "event_type": event_type,
    }
    _validate_event(event)
    timestamp = created_at or datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO events(event_type, city, category, amount, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(event_type).strip(),
                str(city).strip(),
                str(category).strip(),
                float(amount),
                timestamp,
            ),
        )
        return int(cur.lastrowid)


def get_events_after(last_event_id: int, limit: int = 1000) -> List[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, event_type, city, category, amount, created_at
            FROM events
            WHERE id > ?
            ORDER BY id ASC
            LIMIT ?
            """,
            (int(last_event_id), int(limit)),
        ).fetchall()


def get_checkpoint() -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT last_event_id FROM processor_state WHERE id=1"
        ).fetchone()
        return int(row["last_event_id"])


def set_checkpoint(event_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE processor_state SET last_event_id=? WHERE id=1",
            (int(event_id),),
        )


def get_snapshot() -> Dict[str, Any]:
    with get_connection() as conn:
        totals = conn.execute(
            "SELECT total_orders, total_sales, updated_at FROM analytics_totals WHERE id=1"
        ).fetchone()
        cities = conn.execute(
            "SELECT city, orders, sales FROM city_sales ORDER BY sales DESC, city ASC"
        ).fetchall()
        categories = conn.execute(
            "SELECT category, orders, sales FROM category_sales ORDER BY sales DESC, category ASC"
        ).fetchall()

    return {
        "totals": dict(totals) if totals else {
            "total_orders": 0, "total_sales": 0, "updated_at": None
        },
        "cities": [dict(row) for row in cities],
        "categories": [dict(row) for row in categories],
    }


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {get_db_path()}")
