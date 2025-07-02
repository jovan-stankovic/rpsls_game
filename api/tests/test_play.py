import pytest
from fastapi import status

from routers.play import determine_result
from tests.conftest import get_or_create_player


@pytest.mark.parametrize(
    "player_choice, expected_status",
    [
        (0, status.HTTP_400_BAD_REQUEST),  # invalid choice
        (1, status.HTTP_200_OK),  # valid choice
        (2, status.HTTP_200_OK),  # valid choice
        (3, status.HTTP_200_OK),  # valid choice
        (4, status.HTTP_200_OK),  # valid choice
        (5, status.HTTP_200_OK),  # invalid choice
        (6, status.HTTP_400_BAD_REQUEST),  # invalid choice
    ],
)
def test_play_game(player_choice, expected_status, client):
    get_or_create_player()
    test_request = {"player": player_choice}

    response = client.post("/play", json=test_request)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        result_data = response.json()
        assert "result" in result_data
        assert "player_choice" in result_data
        assert "computer_choice" in result_data
        assert result_data["player_choice"] == player_choice
        assert result_data["computer_choice"] in [1, 2, 3, 4, 5]


@pytest.mark.parametrize(
    "player_choice, computer_choice, expected_result",
    [
        (1, 1, "tie"),  # same choices
        (1, 2, "lose"),  # paper beats rock
        (1, 3, "win"),  # rock beats scissors
    ],
)
def test_determine_result(player_choice, computer_choice, expected_result):
    result = determine_result(player_choice, computer_choice)
    assert result == expected_result
