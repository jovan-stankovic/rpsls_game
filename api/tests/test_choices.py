from constants import CHOICES, VALID_INPUT_CHOICES


def test_get_choices(client):
    response = client.get("/choices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == CHOICES


def test_get_choice(client):
    response = client.get("/choice")
    assert response.status_code == 200
    choice = response.json()
    assert "id" in choice and choice["id"] in VALID_INPUT_CHOICES
    assert "name" in choice and choice["name"] in [choice.name for choice in CHOICES]
