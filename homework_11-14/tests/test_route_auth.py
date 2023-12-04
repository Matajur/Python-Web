from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from sqlalchemy.orm.session import Session

from src.conf import messages
from src.database.models import User

# pytest --cov=. --cov-report html tests/ <- to check coverage of the code with tests, results in htmlcov/index.html

# signup


def test_create_user(
    client: TestClient, user: dict[str, str], monkeypatch: MonkeyPatch
):
    mock_send_verification_email = MagicMock()
    monkeypatch.setattr(
        "src.routes.auth.send_verification_email", mock_send_verification_email
    )
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["email"] == user.get("email")


def test_repeat_create_user(
    client: TestClient, user: dict[str, str], monkeypatch: MonkeyPatch
):
    mock_send_verification_email = MagicMock()
    monkeypatch.setattr(
        "src.routes.auth.send_verification_email", mock_send_verification_email
    )
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 409, response.text
    payload = response.json()
    assert payload["detail"] == messages.ACCOUNT_EXISTS


# login


def test_login_user_not_confirmed_email(client: TestClient, user: dict[str, str]):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},  # type: ignore
    )
    assert response.status_code == 401, response.text
    payload = response.json()
    assert payload["detail"] == messages.EMAIL_NOT_VERIFIED


def test_login_user_confirmed_email(
    client: TestClient, user: dict[str, str], session: Session
):
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True  # type: ignore
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},  # type: ignore
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"] != None
    assert payload["refresh_token"] != None


def test_login_user_with_wrong_password(
    client: TestClient, user: dict[str, str], session: Session
):
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()  # type: ignore
    )
    current_user.confirmed = True  # type: ignore
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": "test_password"},  # type: ignore
    )
    assert response.status_code == 401, response.text
    payload = response.json()
    assert payload["detail"] == messages.INVALID_PASSWORD


def test_login_user_with_wrong_email(
    client: TestClient, user: dict[str, str], session: Session
):
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()  # type: ignore
    )
    current_user.confirmed = True  # type: ignore
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": "example@test.com", "password": user.get("password")},  # type: ignore
    )
    assert response.status_code == 401, response.text
    payload = response.json()
    assert payload["detail"] == messages.INVALID_EMAIL


# refresh token
