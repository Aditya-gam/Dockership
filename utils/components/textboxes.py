# Dockership/utils/components/textboxes.py

import streamlit as st  # Import Streamlit for creating the user interface


def create_textbox(label, default_value="", key=None, **kwargs):
    """
    Creates a customizable text input box.

    This function generates a text input field in the Streamlit app, allowing users
    to input text. It can be used for various purposes like entering usernames,
    search queries, or other text-based inputs.

    Args:
        label (str): The label to display next to the textbox.
        default_value (str): The default value for the textbox (default is an empty string).
        key (str, optional): A unique Streamlit key for the widget to manage its state.
                             Useful when multiple textboxes are used.
        **kwargs: Additional keyword arguments to customize the textbox.
                  Examples:
                  - `placeholder` (str): Placeholder text displayed in the input box.
                  - `max_chars` (int): Maximum number of characters allowed.

    Returns:
        str: The text entered by the user in the textbox.
    """
    # Create a Streamlit text input field with the provided configurations
    return st.text_input(label, value=default_value, key=key, **kwargs)


def create_password_box(label, default_value="", key=None, **kwargs):
    """
    Creates a customizable password input box.

    This function generates a password input field in the Streamlit app, where
    user input is masked for privacy. It is commonly used for secure data entry,
    such as passwords or sensitive information.

    Args:
        label (str): The label to display next to the password box.
        default_value (str): The default value for the password box (default is an empty string).
        key (str, optional): A unique Streamlit key for the widget to manage its state.
                             Useful when multiple password boxes are used.
        **kwargs: Additional keyword arguments to customize the password box.
                  Examples:
                  - `max_chars` (int): Maximum number of characters allowed.

    Returns:
        str: The password entered by the user in the password box.
    """
    # Create a Streamlit text input field with masking enabled (type="password")
    return st.text_input(label, value=default_value, type="password", key=key, **kwargs)
