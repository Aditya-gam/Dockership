# Dockership/utils/grid_utils.py

# Import Slot and Container classes for grid representation
from tasks.ship_balancer import Slot, Container
# Validator for ensuring grid integrity
from utils.validators import validate_ship_grid
import streamlit as st  # Streamlit for building the user interface
# Plotly for creating interactive visualizations
import plotly.graph_objects as go


def create_ship_grid(rows, columns):
    """
    Creates a ship grid with the specified number of rows and columns.

    Args:
        rows (int): Number of rows in the grid.
        columns (int): Number of columns in the grid.

    Returns:
        list: A 2D grid (list of lists) containing Slot objects, initialized as empty.
    """
    return [[Slot(None, False, False) for _ in range(columns)] for _ in range(rows)]


def plotly_visualize_grid(grid, title="Ship Grid", key=None):
    """
    Visualizes the ship's container grid layout using Plotly heatmap.

    This function represents the ship grid with different colors and annotations
    for occupied, unused, and unavailable slots.

    Args:
        grid (list of lists): A 2D grid containing Slot objects.
        title (str): The title of the visualization plot.
        key (str): Unique key for the Streamlit chart element, ensuring widget state independence.

    Returns:
        None: Renders the Plotly chart in Streamlit.
    """
    # Validate the grid structure before proceeding
    validate_ship_grid(grid)

    # Initialize data structures for visualization
    z = []  # Stores color values for each grid cell
    hover_text = []  # Stores hover information for each cell
    annotations = []  # Stores text annotations displayed inside cells

    # Iterate through the grid to prepare visualization data
    for row_idx, row in enumerate(grid):
        z_row = []
        hover_row = []
        for col_idx, slot in enumerate(row):
            # Format the coordinates for hover information
            manifest_coord = f"[{row_idx + 1:02},{col_idx + 1:02}]"
            if slot.container:
                # Occupied slot: Display container name and weight
                cell_text = slot.container.name
                hover_info = (
                    f"Coordinates: {manifest_coord}<br>Name: {slot.container.name}<br>Weight: {slot.container.weight}"
                )
                z_row.append(1)  # Color for occupied slots (blue)
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
            elif not slot.available:
                # Unavailable slot: Mark as "NAN"
                cell_text = "NAN"
                hover_info = f"Coordinates: {manifest_coord}<br>NAN"
                z_row.append(-1)  # Color for unavailable slots (light gray)
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
                        # Black text for readability
                        font=dict(size=12, color="black"),
                    )
                )
            else:
                # Unused slot: Leave empty
                cell_text = ""
                hover_info = f"Coordinates: {manifest_coord}<br>UNUSED"
                z_row.append(0)  # Color for unused slots (white)
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
                        # Black text for consistency
                        font=dict(size=12, color="black"),
                    )
                )
            hover_row.append(hover_info)

        # Append processed row data
        z.append(z_row)
        hover_text.append(hover_row)

    # Create a Plotly heatmap for the grid
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            colorscale=[
                [0, "white"],       # Color for unused slots
                [0.5, "lightgray"],  # Color for unavailable slots
                [1, "blue"],        # Color for occupied slots
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
            tickvals=[i for i in range(len(grid[0]))],  # Column indices
            # Human-readable indices
            ticktext=[f"{i + 1:02}" for i in range(len(grid[0]))],
        ),
        yaxis=dict(
            title="Rows",
            showgrid=False,
            zeroline=False,
            tickmode="array",
            tickvals=[i for i in range(len(grid))],  # Row indices
            # Human-readable indices
            ticktext=[f"{i + 1:02}" for i in range(len(grid))],
        ),
        annotations=annotations,  # Add cell annotations
        plot_bgcolor="white",  # Set background color to white
    )

    # Render the Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True, key=key)
