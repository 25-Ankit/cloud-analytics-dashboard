import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB_PATH", str(tmp_path / "events.db"))
    from stream.stream import init_db
    init_db()
    from dashboard.app import app
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_analytics(client):
    response = client.get("/api/analytics")
    assert response.status_code == 200
    assert response.get_json()["totals"]["total_orders"] == 0
