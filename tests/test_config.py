import pytest

from wayweaver.core.config import Settings
from wayweaver.main import create_app

def test_settings_reads_prefixed_environment_variable(
        monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "WAYWEAVER_APP_NAME",
        "WayWeaver Environment Test"
    )

    settings = Settings()

    assert settings.app_name == "WayWeaver Environment Test"

def test_create_app_uses_supplied_settings() -> None:
    settings = Settings(
        app_name = "WayWeaver Environment Test",
        app_env = "test",
        debug = True
    )

    app = create_app(settings)

    assert app.title == "WayWeaver Environment Test"
    assert app.debug is True
    assert app.state.settings is settings