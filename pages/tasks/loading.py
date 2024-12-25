# Dockership/pages/tasks/loading.py

import streamlit as st  # Streamlit for building the frontend
# Functions for loading and unloading containers
from tasks.ship_loader import load_containers, unload_containers
# Functions to manage and visualize the ship grid
from utils.grid_utils import create_ship_grid, plotly_visualize_grid
from utils.components.buttons import (
    create_navigation_button,  # Button to navigate between pages
    create_text_input_with_logging,  # Button for logging custom notes
)
# Manifest-related utilities
from tasks.balancing_utils import convert_grid_to_manifest, append_outbound_to_filename
from utils.logging import log_action  # Function to log user actions
import os  # Standard library for interacting with the operating system


def initialize_session_state(rows, cols):
    """
    Initialize the session state variables for managing the grid, operations, and state transitions.

    Args:
        rows (int): Number of rows in the ship grid.
        cols (int): Number of columns in the ship grid.
    """
    if "ship_grid" not in st.session_state:
        st.session_state.ship_grid = create_ship_grid(
            rows, cols)  # Create the ship grid
    if "messages" not in st.session_state:
        st.session_state.messages = []  # List to store operation messages
    if "total_cost" not in st.session_state:
        st.session_state.total_cost = 0  # Total cost of all operations
    if "container_weights" not in st.session_state:
        # Dictionary to store container weights
        st.session_state.container_weights = {}
    if "loading_step" not in st.session_state:
        # Current step in the loading process
        st.session_state.loading_step = "input_names"
    if "container_names_to_load" not in st.session_state:
        st.session_state.container_names_to_load = []  # List of containers to load
    if "updated_manifest" not in st.session_state:
        st.session_state.updated_manifest = ""  # Updated manifest content
    if "outbound_filename" not in st.session_state:
        # Filename for the updated manifest
        st.session_state.outbound_filename = "manifest.txt"
    if "load_steps" not in st.session_state:
        st.session_state.load_steps = []  # Steps involved in loading containers
    if "unload_steps" not in st.session_state:
        st.session_state.unload_steps = []  # Steps involved in unloading containers


def reset_loading_state():
    """
    Reset the state variables related to the loading process.
    """
    st.session_state.loading_step = "input_names"
    st.session_state.container_names_to_load = []
    st.session_state.container_weights = {}


def loading_task():
    """
    Main function to handle the loading and unloading operations for the ship.
    Allows users to load/unload containers, visualize the grid, update/download the manifest, and log actions.
    """
    # Navigation button to return to the operations page
    col1, _ = st.columns([2, 8])
    with col1:
        if create_navigation_button("Back to Operations", "operation", st.session_state):
            st.rerun()  # Rerun the application to reflect the navigation

    # Page title and user information
    st.title("Ship Loading and Unloading System")
    # Get the username from session state
    username = st.session_state.get("username", "User")

    # Initialize session state variables
    rows, cols = 8, 12  # Default dimensions of the ship grid
    initialize_session_state(rows, cols)

    # Action selection for loading or unloading
    tab = st.radio(
        "Choose Action", ["Load Containers", "Unload Containers"], horizontal=True
    )

    # Visualize grid based on selected action and steps
    if tab == "Load Containers" and st.session_state.load_steps:
        step = st.selectbox(
            "View loading steps:",
            options=[step['name'] for step in st.session_state.load_steps]
        )
        step_data = next(
            s for s in st.session_state.load_steps if s['name'] == step)
        plotly_visualize_grid(step_data['grid'], title=f"Ship Grid - {step}")
        st.info(f"Step Cost: {step_data['cost']} seconds")
        for msg in step_data['messages']:
            st.write(msg)

    elif tab == "Unload Containers" and st.session_state.unload_steps:
        step = st.selectbox(
            "View unloading steps:",
            options=[step['name'] for step in st.session_state.unload_steps]
        )
        step_data = next(
            s for s in st.session_state.unload_steps if s['name'] == step)
        plotly_visualize_grid(step_data['grid'], title=f"Ship Grid - {step}")
        st.info(f"Step Cost: {step_data['cost']} seconds")
        for msg in step_data['messages']:
            st.write(msg)
    else:
        # Display the current ship grid
        plotly_visualize_grid(
            st.session_state.ship_grid, title="Current Ship Grid"
        )

    # Logic for loading containers
    if tab == "Load Containers":
        st.subheader("Load Containers")

        # Step 1: Input container names
        if st.session_state.loading_step == "input_names":
            container_names_input = st.text_input(
                "Container Names (comma-separated)",
                placeholder="Enter container names (e.g., Alpha,Beta,Gamma)"
            )
            if st.button("Next"):
                if container_names_input:
                    container_names = [
                        name.strip() for name in container_names_input.split(",") if name.strip()]
                    if container_names:
                        st.session_state.container_names_to_load = container_names
                        st.session_state.loading_step = "input_weights"
                        st.rerun()
                    else:
                        st.error("Please provide valid container names.")
                else:
                    st.error("Please provide container names.")

        # Step 2: Input container weights
        elif st.session_state.loading_step == "input_weights":
            st.subheader("Enter Container Weights")
            for name in st.session_state.container_names_to_load:
                st.session_state.container_weights[name] = st.number_input(
                    f"Weight for '{name}' (kg):",
                    min_value=0,
                    max_value=99999,
                    step=1,
                    format="%d",
                    key=f"{name}_weight"
                )

            if st.button("Confirm Load"):
                updated_grid, messages, cost, steps = load_containers(
                    st.session_state.ship_grid,
                    st.session_state.container_names_to_load
                )
                st.session_state.ship_grid = updated_grid
                st.session_state.messages.extend(messages)
                st.session_state.total_cost += cost
                st.session_state.load_steps = steps
                reset_loading_state()

                # Log user action
                for name in st.session_state.container_names_to_load:
                    log_action(username=username, action="LOAD",
                               notes=f"{username} loaded {name}")
                st.rerun()

    # Logic for unloading containers
    elif tab == "Unload Containers":
        st.subheader("Unload Containers")
        container_names_input = st.text_input(
            "Container Names to Unload (comma-separated)",
            placeholder="Enter container names (e.g., Alpha,Beta,Gamma)"
        )

        if st.button("Unload Containers"):
            if container_names_input:
                container_names = [name.strip()
                                   for name in container_names_input.split(",")]
                updated_grid, messages, cost, steps = unload_containers(
                    st.session_state.ship_grid, container_names
                )
                st.session_state.ship_grid = updated_grid
                st.session_state.messages.extend(messages)
                st.session_state.total_cost += cost
                st.session_state.unload_steps = steps

                # Log user action
                for name in container_names:
                    log_action(username=username, action="UNLOAD",
                               notes=f"{username} unloaded {name}")
                st.rerun()
            else:
                st.error("Please provide valid container names.")

    # Operation summary and manifest handling
    st.subheader("Operation Summary")
    st.info(f"Total Operation Cost: {st.session_state.total_cost} seconds")

    st.subheader("Update/Download Manifest")
    col1, col2, col3 = st.columns(3)

    # Update Manifest
    with col1:
        if st.button("Update Manifest"):
            updated_manifest = convert_grid_to_manifest(
                st.session_state.ship_grid)
            outbound_filename = append_outbound_to_filename(
                st.session_state.get("file_name", "manifest.txt")
            )
            st.session_state.updated_manifest = updated_manifest
            st.session_state.outbound_filename = outbound_filename
            st.success("Manifest updated successfully!")
            log_action(username=username, action="UPDATE_MANIFEST",
                       notes=f"{username} updated the manifest {outbound_filename}.")

    # Download Manifest
    with col2:
        st.download_button(
            label="Download Updated Manifest",
            data=st.session_state.updated_manifest,
            file_name=st.session_state.outbound_filename,
            mime="text/plain",
            on_click=log_action(username=username, action="DOWNLOAD_MANIFEST",
                                notes=f"{username} downloaded the manifest {st.session_state.outbound_filename}.")
        )

    # Log custom notes
    with col3:
        create_text_input_with_logging(username=username)

    # Display action history
    st.subheader("Action History")
    for msg in st.session_state.messages:
        st.write(msg)
