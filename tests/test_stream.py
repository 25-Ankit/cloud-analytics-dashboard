import os

import pytest


@pytest.fixture
def db(tmp_path, monkeypatch):
    path = tmp_path / "events.db"
    monkeypatch.setenv("ANALYTICS_DB_PATH", str(path))
    from stream.stream import init_db
    init_db()
    return path


def test_put_and_read_event(db):
    from stream.stream import get_events_after, put_event
    event_id = put_event("Mumbai", "Electronics", 100)
    events = get_events_after(0)
    assert event_id == 1
    assert len(events) == 1
    assert events[0]["city"] == "Mumbai"
    assert events[0]["amount"] == 100


def test_invalid_amount(db):
    from stream.stream import put_event
    with pytest.raises(ValueError):
        put_event("Mumbai", "Electronics", -1)
