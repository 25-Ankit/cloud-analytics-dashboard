def test_api_health_and_snapshot(tmp_path,monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB_PATH",str(tmp_path/"events.db"))
    from stream.stream import init_db,put_event
    init_db(); put_event("Mumbai","Electronics",99)
    from processor.processor import process_once
    process_once()
    from dashboard.app import app
    app.config["TESTING"]=True
    c=app.test_client()
    assert c.get("/api/health").status_code==200
    payload=c.get("/api/analytics").get_json(); assert payload["totals"]["total_orders"]==1
