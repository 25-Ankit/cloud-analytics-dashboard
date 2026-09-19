import os,tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as td:
    os.environ["ANALYTICS_DB_PATH"]=str(Path(td)/"events.db")
    from runtime.runtime import EventRuntime
    from processor.processor import process_once
    from stream.stream import get_snapshot
    rt=EventRuntime()
    for i in range(5):
        assert rt.submit({"event_type":"sale","city":"Mumbai","category":"Smoke","amount":10+i})["accepted"]
    assert process_once()==5
    s=get_snapshot(); assert s["totals"]["total_orders"]==5 and s["totals"]["total_sales"]==60
    print("E2E SMOKE PASS",s["totals"])
