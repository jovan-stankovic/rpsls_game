from schemas import Choice

CHOICES: list[Choice] = [
    Choice(id=1, name="rock"),
    Choice(id=2, name="paper"),
    Choice(id=3, name="scissors"),
    Choice(id=4, name="lizard"),
    Choice(id=5, name="spock"),
]

# Valid input choices represent IDs of the game elements
VALID_INPUT_CHOICES: list[int] = [choice.id for choice in CHOICES]

# Define winning conditions where each key beats the choices in its associated list
WIN_CONDITIONS: dict[int, list[int]] = {
    1: [3, 4],  # Rock crushes Scissors and crushes Lizard
    2: [1, 5],  # Paper covers Rock and disproves Spock
    3: [2, 4],  # Scissors cuts Paper and decapitates Lizard
    4: [2, 5],  # Lizard eats Paper and poisons Spock
    5: [1, 3],  # Spock vaporizes Rock and smashes Scissors
}
