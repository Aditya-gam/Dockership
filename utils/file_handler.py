# Dockership/utils/file_handler.py

# Import the logging utility for logging actions
from utils.logging import log_action


def process_file_content(file_content):
    """
    Processes the uploaded file content for further use.

    Args:
        file_content (str): The content of the uploaded file.

    Returns:
        list: A list of lines from the file content, split by line breaks.
    """
    # Split the file content into lines and return as a list
    return file_content.splitlines()


def log_file_upload(username, filename):
    """
    Logs the file upload action.

    Args:
        username (str): The username of the user uploading the file.
        filename (str): The name of the uploaded file.

    Logs:
        An action indicating that the specified user uploaded a file with the given filename.
    """
    log_action(
        username=username,  # The user performing the action
        action="UPLOAD_FILE",  # The type of action being logged
        # Details of the upload action
        notes=f"{username} uploaded file: {filename}",
    )


def log_proceed_to_operations(username):
    """
    Logs the action when the user proceeds to operations.

    Args:
        username (str): The username of the user proceeding to operations.

    Logs:
        An action indicating that the specified user proceeded to operations.
    """
    log_action(
        username=username,  # The user performing the action
        action="PROCEED_TO_OPERATIONS",  # The type of action being logged
        # Details of the operation transition
        notes=f"{username} proceeded to operations.",
    )


def count_containers_on_ship(ship_grid):
    """
    Counts the total number of containers on the ship grid.

    Args:
        ship_grid (list): A 2D grid containing Slot objects representing the ship's layout.

    Returns:
        int: The total count of containers on the ship.
    """
    container_count = 0  # Initialize the container count to zero

    # Iterate through each row of the ship grid
    for row in ship_grid:
        # Iterate through each slot in the row
        for slot in row:
            # Increment the count if the slot contains a container
            if slot.hasContainer:
                container_count += 1

    # Return the total count of containers
    return container_count
