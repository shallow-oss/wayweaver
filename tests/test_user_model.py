from wayweaver.db.base import Base
from wayweaver.models import User


def test_user_model_is_registered_in_metadata() -> None:
    assert "users" in Base.metadata.tables
    assert Base.metadata.tables["users"] is User.__table__


def test_user_model_declares_expected_columns() -> None:
    expected_columns = {
        "id",
        "email",
        "password_hash",
        "display_name",
        "timezone",
        "is_active",
        "created_at",
        "updated_at",
    }

    assert set(User.__table__.columns.keys()) == expected_columns


def test_user_model_declares_primary_key() -> None:
    assert User.__table__.c.id.primary_key is True
    assert User.__table__.c.id.nullable is False
    assert User.__table__.c.id.default is not None


def test_user_model_declares_email_constraint() -> None:
    email_column = User.__table__.c.email

    assert email_column.nullable is False
    assert email_column.unique is True
    assert email_column.type.length == 320


def test_user_model_never_declares_plain_password_column() -> None:
    column_names = set(User.__table__.columns.keys())

    assert "password_hash" in column_names
    assert "password" not in column_names
    assert "plain_password" not in column_names


def test_user_model_declares_defaults() -> None:
    timezone_column = User.__table__.c.timezone
    is_active_column = User.__table__.c.is_active
    created_at_column = User.__table__.c.created_at
    updated_at_column = User.__table__.c.updated_at

    assert timezone_column.default is not None
    assert timezone_column.default.arg == "Asia/Shanghai"
    assert timezone_column.server_default is not None

    assert is_active_column.default is not None
    assert is_active_column.default.arg is True
    assert is_active_column.server_default is not None

    assert created_at_column.server_default is not None
    assert updated_at_column.server_default is not None
    assert updated_at_column.onupdate is not None