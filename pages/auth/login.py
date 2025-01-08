# Dockership/pages/auth/login.py

import streamlit as st  # Import Streamlit for building the user interface

# Import utility components and authentication logic
# Custom button components
from utils.components.buttons import create_button, create_navigation_button
from utils.components.textboxes import create_textbox  # Custom textbox component
# Backend function to validate and check user existence
from auth.login import validate_and_check_user


def login():
    """
    Login page for users.
    Provides a form for users to enter their username, validates the input,
    checks the database for the user, and saves user information to the session state if successful.
    """
    # Page Title and Instructions
    st.title("Dockership Login")  # Display the title of the login page
    # Instructional text for the user
    st.write("Please enter your username to log in:")

    # Username Input Field
    # Render a textbox for username input
    username = create_textbox("Username:")

    # Create two equal-width columns for buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        # Login Button
        if create_button("Login"):  # Render the "Login" button and check if it's clicked
            # Call the backend function to validate the username and check if the user exists
            success, error_message, user = validate_and_check_user(username)

            if not success:
                # If validation or user existence check fails, display an error message
                try:
                    # Use toast notification if supported
                    st.toast(error_message, icon="❌")
                except AttributeError:
                    # Fallback to standard error message display
                    st.error(error_message)
                return  # Exit the function to prevent further processing

            # Save user details to session state if login is successful
            # Store username in session state
            st.session_state.username = user["username"]
            # Store first name in session state
            st.session_state.firstname = user["first_name"]
            st.session_state.page = "file_handler"  # Set the next page to "file_handler"

            # Display a success message welcoming the user
            try:
                # Use toast notification if supported
                st.toast(f"Welcome, {user['first_name']}!", icon="✅")
            except AttributeError:
                # Fallback to standard success message display
                st.success(f"Welcome, {user['first_name']}!")

            # Trigger a rerun to load the next page
            st.rerun()

    with col2:
        # Registration Navigation Button
        create_navigation_button(
            "Need an account? Register here",  # Button label
            "register",  # Target page for navigation
            st.session_state  # Pass session state for navigation management
        )
