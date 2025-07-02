import logging
import random

import requests

from config import RANDOM_NUMBER_SERVICE_URL


def fetch_random_number() -> int | None:
    """
    Fetch a random number from a given URL.

    Returns:
        int | None: The fetched random number, or None if the fetch fails.
    """
    try:
        response = requests.get(RANDOM_NUMBER_SERVICE_URL)
        response.raise_for_status()
        return response.json().get("random_number")
    except requests.RequestException:
        logging.error(
            "Random number service unavailable. Using Python's random lib as fallback."
        )
        return None


def generate_random_number_fallback() -> int:
    """
    Generate a random number using Python's random library as a fallback.

    Returns:
        int: A random number between 1 and 100.
    """
    return random.randint(1, 100)


def map_number_to_choice(number: int) -> int:
    """
    Map a number to a choice index.

    Args:
        number (int): The number to be mapped.

    Returns:
        int: The resulting choice index.
    """
    return number % 5


def get_computer_choice() -> int:
    """
    Get the computer's choice by fetching a random number and mapping it.

    Returns:
        int: The computer's choice index.
    """
    random_number = fetch_random_number()

    if random_number is None:
        random_number = generate_random_number_fallback()

    return map_number_to_choice(random_number)
