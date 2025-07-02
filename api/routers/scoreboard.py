from auth import get_current_player
from database import get_db
from fastapi import APIRouter, Depends
from models import Player, ScoreboardEntry
from schemas import PlayResult
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/scoreboard",
    response_model=list[PlayResult],
    summary="Get player's scoreboard",
    description="Retrieve the last 10 entries from the player's scoreboard.",
)
async def get_scoreboard(
    db: Session = Depends(get_db), current_player: Player = Depends(get_current_player)
) -> list[PlayResult]:
    """
    Fetch the last 10 scoreboard entries for the current player.

    Args:
        db (Session): Database session dependency.
        current_player (Player): The currently authenticated player.

    Returns:
        list[PlayResult]: A list of the most recent 10 game results for the player.
    """
    entries = (
        db.query(ScoreboardEntry)
        .filter(ScoreboardEntry.player_id == current_player.id)
        .order_by(ScoreboardEntry.id.desc())
        .limit(10)
        .all()
    )

    return [
        PlayResult(
            id=entry.id,
            result=entry.result,
            player_choice=entry.player_choice,
            computer_choice=entry.computer_choice,
        )
        for entry in entries
    ]


@router.post(
    "/scoreboard/reset",
    summary="Reset player's scoreboard",
    description="Delete all entries from the player's scoreboard.",
)
async def reset_scoreboard(
    db: Session = Depends(get_db), current_player: Player = Depends(get_current_player)
) -> dict:
    """
    Reset the current player's scoreboard by deleting all entries.

    Args:
        db (Session): Database session dependency.
        current_player (Player): The currently authenticated player.

    Returns:
        dict: A status message indicating successful reset of the scoreboard.
    """
    db.query(ScoreboardEntry).filter(
        ScoreboardEntry.player_id == current_player.id
    ).delete()
    db.commit()
    return {"status": "Scoreboard reset successfully"}
