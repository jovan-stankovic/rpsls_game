from pydantic import BaseModel, Field


class Choice(BaseModel):
    """
    Represents a selectable choice in the game.

    Attributes:
        id (int): Unique identifier for the choice.
        name (str): Name of the choice.
    """

    id: int = Field(..., description="Unique identifier for the choice")
    name: str = Field(..., description="Name of the choice")


class PlayRequest(BaseModel):
    """
    Represents a request to initiate a play session.

    Attributes:
        player (int): Identifier for the initiating player.
    """

    player: int = Field(..., description="Identifier for the initiating player")


class PlayResult(BaseModel):
    """
    Represents the result of a play session.

    Attributes:
        result (str): Outcome of the play (e.g., win, lose, tie).
        player_choice (int): Choice made by the player.
        computer_choice (int): Choice made by the computer.
    """

    result: str = Field(..., description="Outcome of the play")
    player_choice: int = Field(..., description="Choice made by the player")
    computer_choice: int = Field(..., description="Choice made by the computer")


class PlayerCreate(BaseModel):
    """
    Represents the data required to create a new player.

    Attributes:
        name (str): Username of the player.
        password (str): Password for player authentication.
    """

    name: str = Field(..., description="Username of the player")
    password: str = Field(..., description="Password for player authentication")


class PlayerResponse(BaseModel):
    """
    Represents the response received after querying player information.

    Attributes:
        id (int): Unique identifier of the player.
        name (str): Username of the player.
    """

    id: int = Field(..., description="Unique identifier of the player")
    name: str = Field(..., description="Username of the player")


class RefreshTokenRequest(BaseModel):
    """
    Represents the request to refresh an authentication token.

    Attributes:
        refresh_token (str): The refresh token provided during prior authentication. This token is used to request a new access token.
    """

    refresh_token: str = Field(
        ...,
        description="The refresh token provided during prior authentication. This token is used to request a new access token.",
    )
