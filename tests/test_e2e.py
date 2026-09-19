def test_end_to_end(tmp_path,monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB_PATH",str(tmp_path/"events.db"))
    from runtime.runtime import EventRuntime
    from processor.processor import process_once
    from stream.stream import get_snapshot
    rt=EventRuntime()
    for city,cat,amount in [("Mumbai","Electronics",100),("Pune","Grocery",200),("Mumbai","Grocery",50)]:
        result=rt.submit({"event_type":"sale","city":city,"category":cat,"amount":amount})
        assert result["accepted"]
    assert process_once()==3
    snap=get_snapshot()
    assert snap["totals"]["total_orders"]==3
    assert snap["totals"]["total_sales"]==350
    assert process_once()==0
