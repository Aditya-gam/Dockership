# Dockership/auth/register.py

# Import necessary modules and utilities
# Database configuration and connection management
from config.db_config import DBConfig
# Utility function to check if a user exists in the database
from utils.validators import check_user_exists
from utils.logging import log_action  # Logging utility to record user actions

# Initialize the database configuration object
db_config = DBConfig()

# Establish a connection to the MongoDB database
db = db_config.connect()

# Get the users and logs collections from the database
users_collection = db_config.get_collection(
    "users")  # Collection for storing user details
# Collection for storing logs of user actions
logs_collection = db_config.get_collection("logs")


def register_user(first_name: str, last_name: str, username: str):
    """
    Register a new user by adding their details to the users collection.

    This function checks if the username already exists, capitalizes the user's first and last names,
    inserts the user details into the database, and logs the registration action.

    Args:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user. (Optional)
        username (str): The username of the user.

    Returns:
        bool: True if registration is successful, False otherwise.
    """
    # Step 1: Check if the username already exists in the database
    if check_user_exists(username):
        # If the username exists, return False to indicate registration failure
        return False

    # Step 2: Capitalize the first and last names for consistent formatting
    # Capitalize the first letter of the first name
    first_name = first_name.capitalize()
    # Capitalize last name if provided, else set to empty string
    last_name = last_name.capitalize() if last_name else ''

    # Step 3: Insert the user details into the users collection
    users_collection.insert_one({
        "first_name": first_name,  # User's first name
        "last_name": last_name,    # User's last name
        "username": username       # Unique username for the user
    })

    # Step 4: Log the registration action for auditing purposes
    log_action(
        username=username,  # Username of the user who registered
        action="REGISTER",  # Action type being logged
        # Additional details for the log
        notes=f"{username} registered successfully."
    )

    # Step 5: Return True to indicate successful registration
    return True
