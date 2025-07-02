import logging
import os


def get_env_variable(var_name: str) -> str | None:
    """
    Retrieve an environment variable's value.

    Args:
        var_name (str): Name of the environment variable.

    Returns:
        str | None: The value of the environment variable, or None if it's not set.
    """
    value = os.getenv(var_name)
    if value is None:
        logging.warning(f"The environment variable {var_name} is not set.")
    return value


# Environment variables
DATABASE_URL = get_env_variable("DATABASE_URL")
SECRET_KEY = get_env_variable("SECRET_KEY")
ALGORITHM = get_env_variable("ALGORITHM")
RANDOM_NUMBER_SERVICE_URL = get_env_variable("RANDOM_NUMBER_SERVICE_URL")
