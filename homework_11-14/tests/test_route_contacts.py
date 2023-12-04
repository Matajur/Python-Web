import pytest
from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from sqlalchemy.orm.session import Session
from unittest.mock import AsyncMock, MagicMock, patch

from src.conf import messages
from src.database.models import User, Role
from src.services.auth import auth_service

CONTACT = {
    "name": "Super",
    "thurname": "User",
    "email": "user@example.com",
    "phone": "+380991234567",
    "birthday": "2000-10-20",
    "notes": "hello world!",
}

CONTACT_UPD = {
    "name": "Not_So_Super",
    "thurname": "User",
    "email": "user@example.com",
    "phone": "+380991234567",
    "birthday": "2000-10-20",
    "notes": "hello world!",
}


@pytest.fixture()
def acc_token(
    client: TestClient, user: dict[str, str], session: Session, monkeypatch: MonkeyPatch
):
    mock_send_verification_email = MagicMock()
    monkeypatch.setattr(
        "src.routes.auth.send_verification_email", mock_send_verification_email
    )
    client.post("/api/auth/signup", json=user)

    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True  # type: ignore
    current_user.role = Role.admin  # type: ignore
    session.commit()

    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},  # type: ignore
    )
    data = response.json()
    return data["access_token"]  # it returns access_token, refresh_token, token_type


def test_create_contact(client: TestClient, acc_token: str, monkeypatch: MonkeyPatch):
    with patch.object(auth_service, "rds") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.post(
            "/api/contacts",
            json=CONTACT,
            headers={"Authorization": f"Bearer {acc_token}"},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert "id" in data


def test_get_contacts(client: TestClient, acc_token: str, monkeypatch: MonkeyPatch):
    with patch.object(auth_service, "rds") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/contacts", headers={"Authorization": f"Bearer {acc_token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["name"] == CONTACT["name"]


def test_get_next_birthdays(
    client: TestClient, acc_token: str, monkeypatch: MonkeyPatch
):
    with patch.object(auth_service, "rds") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/contacts/next_birthdays",
            headers={"Authorization": f"Bearer {acc_token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["name"] == CONTACT["name"]


def test_get_contact(client: TestClient, acc_token: str, monkeypatch: MonkeyPatch):
    with patch.object(auth_service, "rds") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/contacts/1", headers={"Authorization": f"Bearer {acc_token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == dict
        assert data["name"] == CONTACT["name"]


def test_update_contact(client: TestClient, acc_token: str, monkeypatch: MonkeyPatch):
    with patch.object(auth_service, "rds") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.put(
            "/api/contacts/1",
            json=CONTACT_UPD,
            headers={"Authorization": f"Bearer {acc_token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == CONTACT_UPD["name"]


def test_remove_contact(client: TestClient, acc_token: str, monkeypatch: MonkeyPatch):
    with patch.object(auth_service, "rds") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {acc_token}"},
        )
        assert response.status_code == 204, response.text
