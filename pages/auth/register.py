# Dockership/pages/auth/register.py

import streamlit as st  # Streamlit for building the web interface

# Import custom components and utilities
# Button components
from utils.components.buttons import create_button, create_navigation_button
from utils.components.textboxes import create_textbox  # Textbox component
# Validation utilities for username and names
from utils.validators import validate_username, validate_name
from auth.register import register_user  # Function to register a new user
# Database configuration for connection and collections
from config.db_config import DBConfig

# Initialize the database configuration object
db_config = DBConfig()
db = db_config.connect()  # Connect to the database
logs_collection = db_config.get_collection(
    "logs")  # Retrieve the logs collection


def register():
    """
    Registration page where a new user can create their account.

    This page accepts the user's first name, last name, and username,
    validates the inputs, and attempts to register the user. It provides
    appropriate feedback for both success and failure cases.
    """
    # Page Title
    st.title("User Registration")  # Display the title of the registration page

    # Input Fields
    # Input for the user's first name
    first_name = create_textbox("First Name:")
    last_name = create_textbox("Last Name:")  # Input for the user's last name
    username = create_textbox("Username:")  # Input for the user's username

    # Layout for buttons
    # Create two columns: one for the register button and another for navigation
    col1, col2 = st.columns([1, 6])

    with col1:
        # Register Button
        # Render the "Register" button and check if it's clicked
        if create_button("Register"):
            # Validate First Name
            is_first_name_valid, first_name_error = validate_name(
                first_name, "first_name"
            )
            # Validate Last Name
            is_last_name_valid, last_name_error = validate_name(
                last_name, "last_name"
            )
            # Validate Username
            is_username_valid, username_error = validate_username(username)

            # Display errors if validation fails
            if not is_first_name_valid:
                # Display error for invalid first name
                st.error(first_name_error)
                return
            if not is_last_name_valid:
                # Display error for invalid last name
                st.error(last_name_error)
                return
            if not is_username_valid:
                st.error(username_error)  # Display error for invalid username
                return

            # Attempt to register the user in the database
            if register_user(first_name, last_name, username):
                # Registration successful
                try:
                    # Display a success toast notification if supported
                    st.toast(
                        "Registration successful! Redirecting to login...", icon="✅"
                    )
                except AttributeError:
                    # Fallback to standard success message
                    st.success(
                        "Registration successful! Redirecting to login...")

                # Redirect to login page after successful registration
                create_navigation_button(
                    None, "login", st.session_state, trigger_redirect=True
                )
                st.session_state.page = "login"  # Update session state to navigate to login
                st.rerun()  # Trigger rerun to reload the page
            else:
                # Username already exists
                try:
                    # Display an error toast notification if supported
                    st.toast(
                        "Username already exists. Please choose another.", icon="❌"
                    )
                except AttributeError:
                    # Fallback to standard error message
                    st.error("Username already exists. Please choose another.")

    with col2:
        # Navigation Button for Login Page
        create_navigation_button(
            "Already have an account? Login here",  # Button label
            "login",  # Target page for navigation
            st.session_state,  # Pass session state for navigation management
        )
