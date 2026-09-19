def test_policy_runtime(tmp_path,monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB_PATH",str(tmp_path/"events.db"))
    from runtime.policy import Policy,PolicyEngine
    from runtime.runtime import EventRuntime
    engine=PolicyEngine(Policy(allowed_event_types=frozenset({"sale"}),max_amount=100,rate_limit_per_minute=10))
    rt=EventRuntime(engine)
    ok=rt.submit({"event_type":"sale","city":"Mumbai","category":"X","amount":50})
    bad=rt.submit({"event_type":"sale","city":"Mumbai","category":"X","amount":101})
    assert ok["accepted"] and not bad["accepted"]
