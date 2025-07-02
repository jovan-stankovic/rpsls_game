from fastapi import status

from models import ScoreboardEntry
from tests.conftest import db, get_or_create_player


def test_get_scoreboard(client):
    mock_player = get_or_create_player()
    for i in range(15):
        entry = ScoreboardEntry(
            player_id=mock_player.id,
            result="win",
            player_choice=1,
            computer_choice=3,
        )
        db.add(entry)
    db.commit()

    response = client.get("/scoreboard")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 10  # Only 10 entries should be returned

    for result in response.json():
        assert result["result"] == "win"
        assert result["player_choice"] == 1
        assert result["computer_choice"] == 3


def test_reset_scoreboard(client):
    mock_player = get_or_create_player()
    player_id = mock_player.id
    for i in range(5):
        entry = ScoreboardEntry(
            player_id=player_id,
            result="win",
            player_choice=1,
            computer_choice=3,
        )
        db.add(entry)
    db.commit()

    response = client.post("/scoreboard/reset")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Scoreboard reset successfully"}

    # Verify that the scoreboard is empty for the player
    entries = (
        db.query(ScoreboardEntry).filter(ScoreboardEntry.player_id == player_id).all()
    )
    assert len(entries) == 0
