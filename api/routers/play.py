from auth import get_current_player
from constants import CHOICES, VALID_INPUT_CHOICES, WIN_CONDITIONS
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import Player, ScoreboardEntry
from schemas import PlayRequest, PlayResult
from services import get_computer_choice
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/play",
    response_model=PlayResult,
    dependencies=[Depends(get_current_player)],
    summary="Play a game round",
    description="Play a round against the computer and log the result.",
)
async def play_game(
    request: PlayRequest,
    db: Session = Depends(get_db),
    current_player: Player = Depends(get_current_player),
) -> PlayResult:
    """
    Endpoint to play a game round against the computer.

    Args:
        request (PlayRequest): The player's choice for the game round.
        db (Session): SQLAlchemy session dependency.
        current_player (Player): The current authenticated player.

    Returns:
        PlayResult: Result of the game round, including choices and outcome.

    Raises:
        HTTPException: If the provided player choice is invalid.
    """
    if request.player not in VALID_INPUT_CHOICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid choice: {request.player}. Valid choices are {VALID_INPUT_CHOICES}.",
        )

    computer_choice = CHOICES[get_computer_choice()]
    result = determine_result(request.player, computer_choice.id)

    scoreboard_entry = ScoreboardEntry(
        result=result,
        player_choice=request.player,
        computer_choice=computer_choice.id,
        player_id=current_player.id,
    )
    db.add(scoreboard_entry)
    db.commit()

    return PlayResult(
        result=result,
        player_choice=request.player,
        computer_choice=computer_choice.id,
    )


def determine_result(player_choice: int, computer_choice: int) -> str:
    """
    Determine the result of the game based on player's and computer's choices.

    Args:
        player_choice (int): The choice made by the player.
        computer_choice (int): The choice made by the computer.

    Returns:
        str: The outcome of the game round: either "tie", "win", or "lose".
    """
    if player_choice == computer_choice:
        return "tie"
    if computer_choice in WIN_CONDITIONS[player_choice]:
        return "win"
    return "lose"
