from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.core.security import oauth2_scheme
from app.modules.users.services import UserService
from main import app


def _sample_user_display():
    from app.modules.users.schemas import UserDisplay

    return UserDisplay(
        id=1,
        email="alice@example.com",
        username="alice",
        date_joined=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    )


@pytest.fixture
def mock_user_service() -> MagicMock:
    svc = MagicMock(spec=UserService)
    svc.get_all_users.return_value = [_sample_user_display()]
    svc.get_user.return_value = _sample_user_display()
    svc.register.return_value = _sample_user_display()
    svc.login.return_value = {
        "access_token": "test.jwt.token",
        "token_type": "bearer",
    }
    svc.update.return_value = _sample_user_display()
    svc.delete.return_value = None
    return svc


@pytest.fixture
def client(mock_user_service: MagicMock) -> TestClient:
    def _user_service_override() -> MagicMock:
        return mock_user_service

    async def _oauth2_override() -> str:
        return "Bearer-token-override"

    app.dependency_overrides[UserService] = _user_service_override
    app.dependency_overrides[oauth2_scheme] = _oauth2_override
    try:
        yield TestClient(app, raise_server_exceptions=True)
    finally:
        app.dependency_overrides.clear()
