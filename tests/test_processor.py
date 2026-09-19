def test_incremental_processor_is_atomic(tmp_path,monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB_PATH",str(tmp_path/"events.db"))
    from stream.stream import init_db,put_event,get_checkpoint,get_snapshot
    from processor.processor import process_once
    init_db(); put_event("Mumbai","Electronics",100); put_event("Pune","Grocery",250)
    assert process_once()==2; assert process_once()==0; assert get_checkpoint()==2
    snap=get_snapshot(); assert snap["totals"]["total_orders"]==2; assert snap["totals"]["total_sales"]==350
    put_event("Mumbai","Grocery",50); assert process_once()==1
    snap=get_snapshot(); assert snap["totals"]["total_orders"]==3; assert snap["totals"]["total_sales"]==400
