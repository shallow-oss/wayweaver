from fastapi.testclient import TestClient

from wayweaver.main import create_app


def test_health_live_returns_ok() -> None:
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}