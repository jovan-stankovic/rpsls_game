from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Player(Base):
    """
    Represents a player in the system.

    Attributes:
        id (int): Identifier for the player.
        name (str): Unique username for the player.
        password (str): Password for player authentication.
        wins (int): Number of wins accumulated.
        losses (int): Number of losses accumulated.
        ties (int): Number of ties accumulated.
    """

    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    ties = Column(Integer, default=0)

    scoreboard_entries = relationship("ScoreboardEntry", back_populates="player")


class ScoreboardEntry(Base):
    """
    Represents a scoreboard entry related to a player's game.

    Attributes:
        id (int): Identifier for the scoreboard entry.
        result (str): Result of the game.
        player_choice (int): Choice made by the player.
        computer_choice (int): Choice made by the computer.
        player_id (int): Foreign key reference to the player who owns the entry.
    """

    __tablename__ = "scoreboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    result = Column(String, index=True)
    player_choice = Column(Integer)
    computer_choice = Column(Integer)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    player = relationship("Player", back_populates="scoreboard_entries")


class RefreshToken(Base):
    """
    Represents a refresh token used for token-based authentication.

    Attributes:
        id (int): Identifier for the refresh token.
        token (str): Unique token string.
        player_id (int): Foreign key reference to the player associated with the refresh token.
    """

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    player = relationship("Player", lazy="joined")
