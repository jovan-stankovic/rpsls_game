from services import (
    fetch_random_number,
    generate_random_number_fallback,
    get_computer_choice,
    map_number_to_choice,
)


def test_fetch_random_number():
    random_number = fetch_random_number()

    if random_number is not None:
        assert isinstance(random_number, int)
        assert random_number in list(range(1, 101))


def test_generate_random_number_fallback():
    for _ in range(100):
        number = generate_random_number_fallback()
        assert 1 <= number <= 100


def test_map_number_to_choice():
    # Test ensuring correct modulus-based mapping
    assert map_number_to_choice(1) == 1
    assert map_number_to_choice(99) == 4
    assert map_number_to_choice(100) == 0


def test_get_computer_choice():
    # Test the final decision-making process correctly maps numbers
    choice = get_computer_choice()
    assert choice in [0, 1, 2, 3, 4]  # Ensure outputs are within expected range
