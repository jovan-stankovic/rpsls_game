from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import ALGORITHM, SECRET_KEY
from database import get_db
from models import Player

# Password encryption and verification context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme for OAuth2
oauth2_scheme = APIKeyHeader(name="Authorization")


def get_password_hash(password: str) -> str:
    """
    Hashes a plain password using bcrypt and returns the hashed password.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided plain password matches the hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to check against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, str | datetime]) -> str:
    """
    Creates a JWT access token with an expiration time.

    Args:
        data (dict): Data to encode in the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict[str, str | datetime]) -> str:
    """
    Creates a JWT refresh token with an expiration time.

    Args:
        data (dict): Data to encode in the refresh token.

    Returns:
        str: The encoded JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_player(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Player:
    """
    Retrieve the current player from the database using the JWT token.

    Args:
        token (str): JWT token provided via the OAuth2 scheme.
        db (Session): Database session dependency.

    Returns:
        Player: The authenticated player object.

    Raises:
        HTTPException: If the token is invalid or the player is not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        player = db.query(Player).filter(Player.name == name).first()
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Player not found",
            )
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return player
