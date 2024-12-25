# Dockership/utils/visualizer.py

"""
Utility module for parsing input data and visualizing ship grid layouts.
"""

import numpy as np  # For numerical operations and creating the grid
# (Optional) For additional visualization methods
import matplotlib.pyplot as plt
import streamlit as st  # For Streamlit-based visualizations
import re  # For parsing manifest input lines
import plotly.graph_objects as go  # For creating interactive grid visualizations


def parse_input(input_lines, rows=8, cols=12):
    """
    Parses input data into a grid format.

    Args:
        input_lines (list): List of input lines from the manifest file.
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.

    Returns:
        numpy.ndarray: Parsed grid layout where each cell contains a container name or "UNUSED".
    """
    # Initialize the grid with default value "UNUSED"
    grid = np.full((rows, cols), "UNUSED", dtype=object)

    # Define a regex pattern to extract coordinates and container information
    line_regex = re.compile(r"\[(\d+),(\d+)\]\s*,\s*\{\d+\}\s*,\s*(\w+)")

    for line in input_lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        # Match line format using the regex pattern
        match = line_regex.match(line)
        if match:
            row, col, container = match.groups()
            row, col = int(row), int(col)

            # Convert coordinates to grid indices
            # Reverse row indexing for grid (row 1 is bottom)
            grid_row = rows - row
            grid_col = col - 1  # Convert 1-based to 0-based indexing

            # Check if coordinates are within grid bounds
            if 0 <= grid_row < rows and 0 <= grid_col < cols:
                # Assign the container name to the grid cell
                grid[grid_row, grid_col] = container

    return grid


def plotly_visualize_grid(grid, title="Ship Grid"):
    """
    Visualizes the ship's container grid layout using Plotly with proper text placement inside the blocks.

    Args:
        grid (list of lists): 2D grid containing Slot objects or plain text.
        title (str): Title of the plot.

    Returns:
        plotly.graph_objects.Figure: A Plotly figure object for visualization.
    """
    # Initialize data structures for visualization
    z = []  # Color mapping for grid cells
    hover_text = []  # Hover text for each cell
    annotations = []  # Annotations for text inside cells

    for row_idx, row in enumerate(grid):
        z_row = []
        hover_row = []
        for col_idx, slot in enumerate(row):
            # Format the coordinates for hover information
            manifest_coord = f"[{row_idx + 1:02},{col_idx + 1:02}]"
            if slot != "UNUSED":  # Occupied slot
                cell_text = slot  # The container name
                hover_info = f"Coordinates: {manifest_coord}<br>Container: {slot}"
                z_row.append(1)  # Occupied (blue)
                annotations.append(
                    dict(
                        text=cell_text,
                        x=col_idx,
                        y=row_idx,
                        xref="x",
                        yref="y",
                        showarrow=False,
                        xanchor="center",
                        yanchor="middle",
                        # White text for contrast
                        font=dict(size=12, color="white"),
                    )
                )
            else:  # Unused slot
                cell_text = ""
                hover_info = f"Coordinates: {manifest_coord}<br>UNUSED"
                z_row.append(0)  # UNUSED (white)
                annotations.append(
                    dict(
                        text=cell_text,
                        x=col_idx,
                        y=row_idx,
                        xref="x",
                        yref="y",
                        showarrow=False,
                        xanchor="center",
                        yanchor="middle",
                        # Black text for clarity
                        font=dict(size=12, color="black"),
                    )
                )
            hover_row.append(hover_info)

        z.append(z_row)
        hover_text.append(hover_row)

    # Create a Plotly heatmap for the grid
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            colorscale=[
                [0, "white"],       # Empty slots
                [1, "blue"],        # Occupied slots
            ],
            hoverinfo="text",  # Enable hover information
            text=hover_text,
            showscale=False,  # Hide the color scale for simplicity
        )
    )

    # Configure the layout of the Plotly figure
    fig.update_layout(
        title=dict(text=title, x=0.5),  # Center the title
        xaxis=dict(
            title="Columns",
            showgrid=False,
            zeroline=False,
            tickmode="array",
            tickvals=[i for i in range(len(grid[0]))],
            # Human-readable indices
            ticktext=[f"{i + 1:02}" for i in range(len(grid[0]))],
        ),
        yaxis=dict(
            title="Rows",
            showgrid=False,
            zeroline=False,
            tickmode="array",
            tickvals=[i for i in range(len(grid))],
            # Human-readable indices
            ticktext=[f"{i + 1:02}" for i in range(len(grid))],
        ),
        annotations=annotations,  # Add cell annotations
        plot_bgcolor="white",  # Set background color to white
    )
    return fig
