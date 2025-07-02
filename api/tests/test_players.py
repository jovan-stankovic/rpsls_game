from fastapi import status

from models import Player, RefreshToken
from tests.conftest import db, get_or_create_player


def test_register_player_success(client):
    """Test successful registration of a new player."""
    response = client.post(
        "/register", json={"name": "player", "password": "strongpassword"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "player"
    assert db.query(Player).filter(Player.name == "player").first() is not None


def test_register_player_existing_name(client):
    """Test failure to register a player due to existing name."""
    response = client.post(
        "/register", json={"name": "test_user", "password": "strongpassword"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Name already exists"


def test_login_player_success(client):
    """Test successful login and token generation."""
    response = client.post("/login", json={"name": "test_user", "password": "password"})

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_player_invalid_credentials(client):
    """Test failure due to invalid login credentials."""
    response = client.post(
        "/login", json={"name": "test_user", "password": "wrongpassword"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"


def test_refresh_access_token_success(client):
    db.query(RefreshToken).delete()
    db.commit()
    get_or_create_player()
    login_response = client.post(
        "/login", json={"name": "test_user", "password": "password"}
    )
    refresh_token = login_response.json().get("refresh_token")

    assert refresh_token is not None, "Refresh token not included in login response"

    refresh_response = client.post("/refresh", json={"refresh_token": refresh_token})
    assert refresh_response.status_code == status.HTTP_200_OK
    assert "access_token" in refresh_response.json()
    assert refresh_response.json()["token_type"] == "bearer"


def test_refresh_access_token_invalid_token(client):
    get_or_create_player()
    refresh_response = client.post(
        "/refresh", json={"refresh_token": "invalid_refresh_token"}
    )
    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert refresh_response.json()["detail"] == "Invalid token"


{"access_token": "token", "refresh_token": "r_token", "token_type": "bearer"}
