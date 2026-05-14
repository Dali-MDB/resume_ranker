from __future__ import annotations

from unittest.mock import MagicMock

from fastapi.testclient import TestClient


def test_get_all_users(client: TestClient, mock_user_service: MagicMock) -> None:
    response = client.get("/users", params={"skip": 0, "limit": 20})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == 1
    assert body[0]["email"] == "alice@example.com"
    mock_user_service.get_all_users.assert_called_once_with(0, 20)


def test_get_user_by_id(client: TestClient, mock_user_service: MagicMock) -> None:
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["username"] == "alice"
    mock_user_service.get_user.assert_called_once_with(1)


def test_register_user(client: TestClient, mock_user_service: MagicMock) -> None:
    payload = {
        "email": "bob@example.com",
        "username": "bob",
        "password": "secret123",
    }
    response = client.post("/users/register", json=payload)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    mock_user_service.register.assert_called_once()
    called = mock_user_service.register.call_args[0][0]
    assert called.email == payload["email"]
    assert called.username == payload["username"]
    assert called.password == payload["password"]


def test_login(client: TestClient, mock_user_service: MagicMock) -> None:
    response = client.post(
        "/users/login",
        data={"username": "alice@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"] == "test.jwt.token"
    mock_user_service.login.assert_called_once()


def test_update_user(client: TestClient, mock_user_service: MagicMock) -> None:
    payload = {"email": "new@example.com", "username": "alice2"}
    response = client.put("/users/1", json=payload)

    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"
    mock_user_service.update.assert_called_once()
    args, _ = mock_user_service.update.call_args
    assert args[0] == 1


def test_delete_user(client: TestClient, mock_user_service: MagicMock) -> None:
    response = client.delete("/users/1")

    assert response.status_code == 200
    assert response.json()["message"] == "the user has been deleted successfully"
    mock_user_service.delete.assert_called_once_with(1)


def test_get_users_protected_path_conflicts_with_user_id_route(client: TestClient) -> None:
    """`/{user_id}` is registered before `/protected`, so this path is parsed as user_id."""
    response = client.get("/users/protected")

    assert response.status_code == 422
