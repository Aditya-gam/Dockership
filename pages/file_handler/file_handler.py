# Dockership/pages/file_handler/file_handler.py

import streamlit as st  # Streamlit for building the web application frontend
from utils.file_handler import (
    process_file_content,  # Function to process the content of the uploaded file
    log_file_upload,  # Function to log file upload events
    log_proceed_to_operations,  # Function to log navigation to operations
    count_containers_on_ship,  # Function to count the number of containers on the ship
)
# Function to validate file content
from utils.validators import validate_file_content
from utils.components.buttons import (
    create_button,  # Function to create custom buttons
    create_logout_button,  # Function to create a logout button
    create_log_file_download_button,  # Function to create a log file download button
)
# Functions for grid creation and validation
from utils.grid_utils import create_ship_grid, validate_ship_grid
from utils.logging import log_action  # Function to log user actions
# Function to update the ship grid with container data
from tasks.ship_balancer import update_ship_grid
# Database configuration class for connection and collections
from config.db_config import DBConfig

# Initialize database connection
db_config = DBConfig()
db = db_config.connect()  # Connect to the database
logs_collection = db_config.get_collection(
    "logs")  # Retrieve the logs collection


def file_handler():
    """
    File Handler page for the Dockership application.

    Allows users to upload a file, processes the file to initialize a ship grid,
    validates the grid, counts containers on the ship, and navigates to the next page.
    """
    # Page Title
    st.title("File Handler")  # Display the title of the page

    # Welcome Message
    # Get the logged-in user's username
    username = st.session_state.get("username", "User")
    # Get the logged-in user's first name
    first_name = st.session_state.get("firstname", "User")
    st.write(f"Hello, {first_name}!")  # Display a personalized welcome message

    # File Uploader
    uploaded_file = st.file_uploader(
        "Upload a .txt file to proceed:", type=["txt"]
    )  # Allow users to upload only .txt files

    if uploaded_file:
        # Read and decode the file content
        file_content = uploaded_file.read().decode("utf-8")
        filename = uploaded_file.name

        # Log the file upload event
        log_file_upload(username, filename)

        # Validate the file content
        is_valid, error_message = validate_file_content(file_content)
        if not is_valid:
            # Display error if validation fails
            st.error(error_message)
            return

        # Process file content and initialize the ship grid
        file_lines = process_file_content(file_content)
        # Store the raw manifest content in session state
        st.session_state.file_content = file_content
        st.session_state.filename = filename  # Store the file name in session state

        # Initialize ship grid and container list if not already initialized
        if "ship_grid" not in st.session_state:
            st.session_state.ship_grid = create_ship_grid(
                8, 12
            )  # Create an 8x12 grid for the ship
        if "containers" not in st.session_state:
            st.session_state.containers = []  # Initialize an empty container list

        # Update the ship grid with container data from the file
        update_ship_grid(
            file_lines, st.session_state.ship_grid, st.session_state.containers
        )

        # Validate the grid structure
        try:
            validate_ship_grid(st.session_state.ship_grid)
        except ValueError as e:
            # Display error if grid validation fails
            st.error(f"Grid validation failed: {e}")
            return

        # Count the number of containers on the ship
        container_count = count_containers_on_ship(st.session_state.ship_grid)
        log_action(
            username=username,
            action="COUNT_CONTAINERS",
            notes=f"Manifest {filename} processed. Total containers: {container_count}",
        )  # Log the container count

        # Display success message and processed data
        st.success("File processed successfully!")
        st.write(f"File Name: {filename}")  # Display the file name
        # Display the number of lines in the file
        st.write(f"Total Lines in File: {len(file_lines)}")
        # Display the container count
        st.write(f"Total Containers on Ship: {container_count}")
        # Display a preview of the file content
        st.write("Preview of Uploaded File:")
        # Show the first 10 lines of the file
        st.text("\n".join(file_lines[:10]))

        # Navigation to the next page
        if create_button("Proceed to Operations"):
            log_proceed_to_operations(username)  # Log navigation to operations
            # Update session state to navigate to the operations page
            st.session_state.page = "operation"
            st.rerun()  # Trigger a rerun to reload the application

    # Create two columns for additional buttons
    col1, col2 = st.columns([1, 1])  # Create two equal-width columns

    with col1:
        # Button to download log files
        create_log_file_download_button()

    with col2:
        # Logout button
        create_logout_button(st.session_state.get(
            "username", "User"), st.session_state)
