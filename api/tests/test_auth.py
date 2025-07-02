from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import jwt
import math
import pytest
from auth import (
    create_access_token,
    create_refresh_token,
    get_current_player,
    get_password_hash,
    verify_password,
)
from config import ALGORITHM, SECRET_KEY
from fastapi import HTTPException, status
from models import Player


@pytest.fixture
def mock_session():
    return Mock()


def test_get_password_hash():
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)

    assert hashed_password != password
    assert hashed_password.startswith("$2b$")  # Bcrypt prefix


def test_verify_password():
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


@patch("auth.datetime")
def test_create_access_token(mock_datetime):
    now = datetime.now()
    mock_datetime.now.return_value = now

    data = {"sub": "test_user"}
    token = create_access_token(data)

    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_data["sub"] == "test_user"
    assert math.isclose(
        decoded_data["exp"], (now + timedelta(minutes=15)).timestamp(), rel_tol=1e-9
    )


@patch("auth.datetime")
def test_create_refresh_token(mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 7, 1, 12, 00, 00)

    data = {"sub": "test_user"}
    token = create_refresh_token(data)

    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_data["sub"] == "test_user"
    assert decoded_data["exp"] == datetime(2025, 7, 2, 12, 00, 00).timestamp()


def test_get_current_player(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = Player(
        id=1, name="test_user"
    )

    token_data = {"sub": "test_user"}
    valid_token = create_access_token(token_data)

    player = get_current_player(token=valid_token, db=mock_session)
    assert player.name == "test_user"

    mock_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_current_player(token=valid_token, db=mock_session)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Player not found"


def test_get_current_player_invalid_token(mock_session):
    invalid_token = "invalidtoken"

    with pytest.raises(HTTPException) as excinfo:
        get_current_player(token=invalid_token, db=mock_session)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate credentials"
