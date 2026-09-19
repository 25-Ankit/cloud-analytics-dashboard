import pytest

def test_event_roundtrip(tmp_path,monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB_PATH",str(tmp_path/"events.db"))
    from stream.stream import init_db,put_event,get_events_after
    init_db(); eid=put_event("Mumbai","Electronics",100)
    rows=get_events_after(0); assert eid==1 and len(rows)==1 and rows[0]["amount"]==100

def test_invalid_amount(tmp_path,monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB_PATH",str(tmp_path/"events.db"))
    from stream.stream import init_db,put_event
    init_db()
    with pytest.raises(ValueError): put_event("Mumbai","X",-1)
