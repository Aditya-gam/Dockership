# Dockership/utils/state_manager.py

"""
Utility module for managing Streamlit session state.
"""


class StateManager:
    """
    Manages Streamlit session state, including page navigation and persistent state variables.

    This utility class helps manage Streamlit's session state, which does not persist across page refreshes by default.
    It provides a simple interface for setting and retrieving the current page and other session state variables.
    """

    def __init__(self, session_state):
        """
        Initializes the StateManager with the given session state.

        Args:
            session_state (streamlit.session_state): The Streamlit session state object.

        Ensures that the default page is set to "login" if it is not already defined in the session state.
        """
        self.session_state = session_state
        if "page" not in self.session_state:
            self.session_state.page = "login"  # Default page is set to "login"

    def set_page(self, page_name):
        """
        Sets the current page in the session state.

        Args:
            page_name (str): The name of the page to navigate to.
        """
        self.session_state.page = page_name

    def get_page(self):
        """
        Retrieves the current page from the session state.

        Returns:
            str: The name of the current page.
        """
        return self.session_state.page
