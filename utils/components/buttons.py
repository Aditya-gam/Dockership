# Dockership/utils/components/buttons.py

import streamlit as st  # Streamlit for building the UI
# Import log file creation and action logging utilities
from utils.logging import create_logs_file, log_action
import os  # For file handling


def create_button(label, on_click=None, args=None, **kwargs):
    """
    Creates a customizable Streamlit button.

    Args:
        label (str): The text to display on the button.
        on_click (function, optional): Function to call when the button is clicked.
        args (tuple, optional): Arguments to pass to the `on_click` function.
        **kwargs: Additional keyword arguments for button customization.

    Returns:
        bool: Whether the button was clicked.
    """
    button = st.button(label, on_click=on_click, args=args, **kwargs)
    return button


def generate_and_download_log_file():
    """
    Generates the log file, provides notifications, and starts the download process.
    """
    # Step 1: Generate the log file
    file_path = create_logs_file()

    if file_path:
        # Notify the user about successful file creation
        try:
            st.toast("✅ Log file created successfully!")
        except AttributeError:
            st.success("✅ Log file created successfully!")

        # Step 2: Provide a download link for the generated file
        with open(file_path, "rb") as file:
            file_contents = file.read()
            st.download_button(
                label="📥 Download Log File",
                data=file_contents,
                file_name=os.path.basename(file_path),
                mime="text/plain",
                help="Download the generated log file"
            )
            try:
                st.toast("📥 Download started!")
            except AttributeError:
                st.info("📥 Download started!")
    else:
        # Notify the user if file generation failed
        st.error("❌ Failed to generate the log file. Please try again.")


def create_log_file_download_button():
    """
    Creates a button that triggers the log file generation and download process.
    """
    return create_button("Generate Log File", on_click=generate_and_download_log_file)


def create_navigation_button(label, page_name, session_state, trigger_redirect=False, **kwargs):
    """
    Creates a navigation button that changes the page in the session state.

    Args:
        label (str): The text to display on the button.
        page_name (str): The page name to navigate to.
        session_state (dict): The Streamlit session state.
        trigger_redirect (bool): If True, navigates immediately without a button click.
        **kwargs: Additional keyword arguments for button customization.

    Returns:
        bool: Whether the button was clicked (only for non-trigger_redirect mode).
    """
    def navigate():
        session_state["page"] = page_name

    if trigger_redirect:
        navigate()  # Immediately set the navigation page.
    else:
        return create_button(label, on_click=navigate, **kwargs)


def create_logout_button(username: str, session_state):
    """
    Creates a logout button that clears the session state and redirects to the login page.

    Args:
        username (str): The username of the user logging out.
        session_state (dict): The Streamlit session state.

    Returns:
        bool: Whether the logout button was clicked.
    """
    def logout():
        # Clear all session state variables and redirect to login page
        session_state.clear()
        session_state["page"] = "login"

        # Log the logout action
        log_action(username=username, action="LOGOUT",
                   notes=f"{username} logged out.")

        # Notify the user about logout
        try:
            st.toast("Logout successful!", icon="✅")
        except AttributeError:
            st.success("Logout successful!")

    return create_button("Logout", on_click=logout)


def create_centered_buttons(label_left, label_right, action_left, action_right):
    """
    Creates two buttons on the same horizontal line, centered on the page.

    Args:
        label_left (str): Text for the left button.
        label_right (str): Text for the right button.
        action_left (function): Function to execute on clicking the left button.
        action_right (function): Function to execute on clicking the right button.

    Returns:
        str: "left_clicked" or "right_clicked" based on which button is clicked.
    """
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if create_button(label_left, on_click=action_left):
            return "left_clicked"

    with col2:
        if create_button(label_right, on_click=action_right):
            return "right_clicked"

    return None


def log_text_input_action(username: str, text: str):
    """
    Logs the user-entered text to the logs collection in MongoDB.

    Args:
        username (str): The username of the user.
        text (str): The text entered by the user.
    """
    if text.strip():  # Ensure the text is not empty
        log_action(username, "USER INPUT LOG", text)
        try:
            st.toast("✅ Note successfully logged!", icon="📝")
        except AttributeError:
            st.success("✅ Note successfully logged!")
    else:
        st.error("❌ Note cannot be empty. Please enter some text.")


def create_text_input_with_logging(username: str):
    """
    Creates a button to reveal a text input box and another button to log the input.

    Args:
        username (str): The username of the user.
    """
    # Step 1: Display the first button to reveal the textbox
    if "show_text_input" not in st.session_state:
        st.session_state.show_text_input = False

    def reveal_text_input():
        st.session_state.show_text_input = True

    create_button("Add a Note", on_click=reveal_text_input)

    # Step 2: Show the text area and log button if enabled
    if st.session_state.show_text_input:
        user_input = st.text_area(
            "Enter your text here:", key="user_text_input")

        def log_note_action():
            log_text_input_action(username, user_input)
            st.session_state.show_text_input = False  # Hide the input area after logging

        create_button("Log Note", on_click=log_note_action)
