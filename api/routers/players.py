import jwt
from auth import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from config import ALGORITHM, SECRET_KEY
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import Player, RefreshToken
from schemas import PlayerCreate, PlayerResponse, RefreshTokenRequest
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/register",
    response_model=PlayerResponse,
    summary="Register a new player",
    description="Create a new player account with a unique username and hashed password.",
)
def register_player(
    player: PlayerCreate, db: Session = Depends(get_db)
) -> PlayerResponse:
    """
    Register a new player in the system.

    Args:
        player (PlayerCreate): New player data including name and password.
        db (Session): SQLAlchemy session dependency.

    Returns:
        PlayerResponse: The registered player's ID and name.

    Raises:
        HTTPException: If the provided username already exists.
    """
    player_in_db = db.query(Player).filter(Player.name == player.name).first()
    if player_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name already exists"
        )

    hashed_password = get_password_hash(player.password)
    new_player = Player(name=player.name, password=hashed_password)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return PlayerResponse(id=new_player.id, name=new_player.name)


@router.post(
    "/login",
    summary="Log in a player",
    description="Authenticate a player and return access and refresh tokens.",
)
def login_player(player: PlayerCreate, db: Session = Depends(get_db)) -> dict:
    """
    Authenticate a player and generate tokens.

    Args:
        player (PlayerCreate): Player's login credentials.
        db (Session): SQLAlchemy session dependency.

    Returns:
        dict: Access and refresh tokens with token type.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    player_in_db = db.query(Player).filter(Player.name == player.name).first()
    if not player_in_db or not verify_password(player.password, player_in_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": player.name})
    refresh_token = create_refresh_token(data={"sub": player.name})

    db.add(RefreshToken(token=refresh_token, player_id=player_in_db.id))
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Generate a new access token using a refresh token.",
)
def refresh_access_token(
    token: RefreshTokenRequest, db: Session = Depends(get_db)
) -> dict:
    """
    Generate a new access token using a valid refresh token.

    Args:
        token (RefreshTokenRequest): JWT refresh token objects.
        db (Session): SQLAlchemy session dependency.

    Returns:
        dict: New access token with token type.

    Raises:
        HTTPException: If the refresh token is invalid, expired, or not found.
    """
    try:
        payload = jwt.decode(token.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        name = payload.get("sub")
        if name is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        refresh_token_in_db = (
            db.query(RefreshToken)
            .filter(RefreshToken.token == token.refresh_token)
            .first()
        )
        if not refresh_token_in_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found",
            )

        new_access_token = create_access_token(data={"sub": name})
        return {"access_token": new_access_token, "token_type": "bearer"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
