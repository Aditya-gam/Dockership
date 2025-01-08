# Dockership/tasks/operator.py

from utils.logging import log_action  # Utility for logging user actions
# Database configuration for managing connections
from config.db_config import DBConfig

# Initialize the database connection
db_config = DBConfig()
db = db_config.connect()  # Establish a connection to the database
# Retrieve the logs collection for logging user actions
logs_collection = db_config.get_collection("logs")


def perform_operation(username: str, operation_type: str):
    """
    Logs the operation action and updates session state for navigation.

    Args:
        username (str): The username of the current user initiating the operation.
        operation_type (str): The type of operation to perform (e.g., "loading", "balancing").

    Returns:
        str: The page to navigate to after the operation is initiated.

    Raises:
        ValueError: If an invalid operation type is provided.
    """
    # Map operation types to their respective descriptions
    operation_map = {
        "loading": "Loading/Unloading containers",  # Description for loading operation
        "balancing": "Balancing the ship's load",  # Description for balancing operation
    }

    # Validate that the provided operation type is valid
    if operation_type not in operation_map:
        # Raise an error for invalid operation types
        raise ValueError(f"Invalid operation type: {operation_type}")

    # Log the user's operation action
    log_action(
        username=username,  # The username of the user initiating the action
        action="OPERATION",  # The type of action being logged
        # Details about the operation
        notes=f"User initiated the {operation_map[operation_type]} operation.",
    )

    # Return the corresponding page name for navigation
    return operation_type
