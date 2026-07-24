from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from wayweaver.db.session import get_db
from wayweaver.main import create_app


def test_health_live_returns_ok() -> None:
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_ready_returns_ok_when_database_is_available() -> None:
    app = create_app()
    # 创建一个假的异步 Session
    mock_session = AsyncMock(spec=AsyncSession)

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            response = client.get("/health/ready")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_session.execute.assert_awaited_once()


def test_health_ready_returns_503_when_database_is_unavailable() -> None:
    app = create_app()
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.side_effect = SQLAlchemyError(
        "database unavailable"
    )

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            response = client.get("/health/ready")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Database is not ready",
    }
    mock_session.execute.assert_awaited_once()