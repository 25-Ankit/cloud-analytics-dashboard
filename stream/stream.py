import sqlite3
import json
from datetime import datetime
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "events.db")


def create_stream():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_data TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def put_event(event):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "INSERT INTO events (event_data, created_at) VALUES (?, ?)",
        (
            json.dumps(event),
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


def get_events():
    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        "SELECT id, event_data, created_at FROM events ORDER BY id"
    ).fetchall()

    conn.close()

    return rows


if __name__ == "__main__":
    create_stream()
    print("Local Kinesis stream is ready!")