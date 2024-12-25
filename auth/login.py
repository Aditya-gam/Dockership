# Dockership/auth/login.py

# Import necessary modules and utilities
# Database configuration and connection management
from config.db_config import DBConfig
# Username validation and existence check utilities
from utils.validators import validate_username, check_user_exists
from utils.logging import log_action  # Logging utility to log user actions

# Initialize the database configuration object
db_config = DBConfig()

# Establish a connection to the MongoDB database
db = db_config.connect()

# Get the users and logs collections from the database
# Collection for storing user information
users_collection = db_config.get_collection("users")
# Collection for storing logs of user actions
logs_collection = db_config.get_collection("logs")


def validate_and_check_user(username: str):
    """
    Validate the username and check if the user exists in the database.

    This function ensures the provided username meets validation criteria,
    checks if the user exists in the database, and logs a successful login action if applicable.

    Args:
        username (str): The username to validate and check.

    Returns:
        tuple: A tuple containing:
            - (bool): Whether the validation and existence check were successful.
            - (str): An error message if validation or existence check fails; empty if successful.
            - (dict or None): The user document from the database if the user exists; None otherwise.
    """
    # Step 1: Validate the username using the validate_username utility
    is_valid, error_message = validate_username(username)
    if not is_valid:
        # If validation fails, return False, the error message, and None for the user document
        return False, error_message, None

    # Step 2: Check if the username exists in the database using the check_user_exists utility
    user = check_user_exists(username)
    if not user:
        # If the user does not exist, return False, an error message, and None
        return False, "Username not found. Please register.", None

    # Step 3: Log the successful user action
    log_action(
        username=username,  # Username of the user logging in
        action="LOGIN",  # Action type being logged
        # Additional notes for the log
        notes=f"{username} logged in successfully."
    )

    # Step 4: Return success, an empty error message, and the user document
    return True, "", user
