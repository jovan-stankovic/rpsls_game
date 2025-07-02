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
