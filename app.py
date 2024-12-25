# Dockership/app.py

import os  # OS module for environment variable handling
# Module to load environment variables from a .env file
from dotenv import load_dotenv
import streamlit as st  # Streamlit for the web application framework

# Import necessary modules and components
from pages.tasks.balancing import balancing_page  # Balancing page logic
from pages.tasks.loading import loading_task  # Loading task page logic
from pages.tasks.operation import operation  # Operation page logic
from pages.file_handler.file_handler import file_handler  # File handler page logic
from pages.auth.register import register  # User registration page logic
from pages.auth.login import login  # User login page logic
from utils.state_manager import StateManager  # Session state management
# Utility function for creating ship grids
from utils.grid_utils import create_ship_grid
# Database configuration and connection management
from config.db_config import DBConfig


# Set the page configuration for Streamlit
# Sets the title of the page and ensures the layout spans the full width
st.set_page_config(page_title="Dockership Application", layout="wide")

# Load environment variables from a .env file
# Ensures sensitive information like database credentials are securely loaded
load_dotenv()

# Initialize the database configuration object
db_config = DBConfig()

# Establish a connection to the MongoDB database
db = db_config.connect()

# Check the database connection status
if not db_config.check_connection():
    # Display an error message on the sidebar if the connection fails
    st.sidebar.error("❌ Failed to connect to MongoDB.")
    st.stop()  # Stop the application as database connection is critical

# Initialize the session state manager
# Manages the application state across multiple pages
state_manager = StateManager(st.session_state)


def render_page(page_name):
    """
    Renders the appropriate page based on the provided page_name.

    Parameters:
    page_name (str): The name of the page to be rendered.
    """
    # Mapping of page names to their corresponding functions
    page_mapping = {
        "login": login,  # Login page
        "register": register,  # Registration page
        "file_handler": file_handler,  # File handler page
        "operation": operation,  # Operations page
        "loading": loading_task,  # Loading task page
        "balancing": balancing_page  # Balancing page
    }

    # Render the page function corresponding to the given page name
    # Defaults to the login page if the page name is not recognized
    page_mapping.get(page_name, login)()


# Main application execution starts here
if __name__ == "__main__":
    # Set up initial configurations for the application
    # Define the dimensions for the ship's grid
    rows, cols = 8, 12

    # Check if the ship grid is already initialized in the session state
    if "ship_grid" not in st.session_state:
        # Create a new ship grid and store it in the session state
        st.session_state.ship_grid = create_ship_grid(
            rows, cols)  # A utility function initializes an 8x12 grid for ship containers

    # Determine the current page based on the session state and render it
    render_page(state_manager.get_page())
