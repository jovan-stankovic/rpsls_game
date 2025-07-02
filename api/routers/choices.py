from auth import get_current_player
from constants import CHOICES
from fastapi import APIRouter, Depends
from schemas import Choice
from services import get_computer_choice

router = APIRouter()


@router.get(
    "/choices",
    response_model=list[Choice],
    dependencies=[Depends(get_current_player)],
    summary="Retrieve all game choices",
    description="Fetch a list of all available choices for the game.",
)
async def get_choices() -> list[Choice]:
    """
    Endpoint to retrieve all available game choices.

    Returns:
        list[Choice]: A list of available choices in the game.
    """
    return CHOICES


@router.get(
    "/choice",
    response_model=Choice,
    dependencies=[Depends(get_current_player)],
    summary="Retrieve a random choice",
    description="Fetch a random choice based on the computer's decision.",
)
async def get_choice() -> Choice:
    """
    Endpoint to retrieve a random choice made by the computer.

    Returns:
        Choice: The computer's selection from available choices.
    """
    choice_index = get_computer_choice()
    return CHOICES[choice_index]
