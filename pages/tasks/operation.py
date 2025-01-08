# Dockership/pages/tasks/operation.py

import streamlit as st  # Import Streamlit for building the user interface
# Utility buttons for navigation and logout
from utils.components.buttons import create_navigation_button, create_logout_button
# Function to perform operations based on user selection
from tasks.operation import perform_operation
# Manages the application state across pages
from utils.state_manager import StateManager
from utils.logging import log_action  # Function to log user actions


def operation():
    """
    Operations page for selecting a task to perform.

    Allows users to choose between loading/unloading and balancing operations.
    Provides options to upload another file or log out.
    """
    # Retrieve session state and user information
    # Initialize the StateManager with the current session state
    state_manager = StateManager(st.session_state)
    # Get the username from session state (default to "User")
    username = st.session_state.get("username", "User")
    # Get the first name from session state (default to "User")
    first_name = st.session_state.get("firstname", "User")

    # Display welcome text
    st.title("Operations")  # Page title
    st.subheader(f"Welcome, {first_name}!")  # Personalized greeting
    # Instruction for the user
    st.write("What operation would you like to perform?")

    # Apply custom button styling for uniform size
    st.markdown(
        "<style>div.row-widget.stButton > button { width: 100%; height: 50px; }</style>",
        unsafe_allow_html=True
    )

    # Create a container for the main buttons
    # Container to group buttons for layout management
    button_container = st.container()
    with button_container:
        # First row: Operation selection buttons
        # Two equally spaced columns for operation buttons
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            # Button for Loading/Unloading Operation
            if st.button("Loading/Unloading Operation"):
                # Trigger the "loading" operation
                next_page = perform_operation(username, "loading")
                # Update session state with the next page
                state_manager.set_page(next_page)
                st.rerun()  # Reload the page to reflect navigation
        with col2:
            # Button for Balancing Operation
            if st.button("Balancing Operation"):
                # Trigger the "balancing" operation
                next_page = perform_operation(username, "balancing")
                # Update session state with the next page
                state_manager.set_page(next_page)
                st.rerun()  # Reload the page to reflect navigation

        # Add spacing between rows
        st.markdown("<br>", unsafe_allow_html=True)

        # Second row: Footer buttons (Upload Another File and Logout)
        # Two equally spaced columns for footer buttons
        col3, col4 = st.columns([1, 1], gap="large")
        with col3:
            # Button for uploading another file
            if create_navigation_button(
                label="Upload Another File",  # Button label
                page_name="file_handler",  # Target page for navigation
                session_state=st.session_state  # Current session state for navigation handling
            ):
                # Clear file content from session state if it exists
                if "file_content" in st.session_state:
                    del st.session_state.file_content
                st.rerun()  # Reload the page to navigate to the File Handler
                # Log the action for auditing
                log_action(
                    username=username,
                    action="Upload Another File",
                    notes=f"{username} requested to upload another file"
                )

        with col4:
            # Logout button
            # Render the logout button
            create_logout_button(username, st.session_state)
