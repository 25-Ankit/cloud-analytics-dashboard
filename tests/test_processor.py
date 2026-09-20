import pytest


@pytest.fixture
def setup_db(tmp_path, monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB_PATH", str(tmp_path / "events.db"))
    from stream.stream import init_db
    init_db()


def test_incremental_processing(setup_db):
    from stream.stream import put_event, get_checkpoint, get_snapshot
    from processor.processor import process_once

    put_event("Mumbai", "Electronics", 100)
    put_event("Pune", "Grocery", 250)

    assert process_once() == 2
    assert process_once() == 0

    snap = get_snapshot()
    assert snap["totals"]["total_orders"] == 2
    assert snap["totals"]["total_sales"] == 350
    assert get_checkpoint() == 2

    put_event("Mumbai", "Grocery", 50)
    assert process_once() == 1

    snap = get_snapshot()
    assert snap["totals"]["total_orders"] == 3
    assert snap["totals"]["total_sales"] == 400
