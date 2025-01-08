# Dockership/utils/components/grid.py

import numpy as np  # Import NumPy for array manipulation


def create_grid_layout(rows, cols, default_value="UNUSED"):
    """
    Creates a grid with the specified rows and columns, filled with a default value.

    This function is useful for initializing a grid-like structure to represent
    layouts such as ship grids, warehouse layouts, or seating arrangements.

    Args:
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
        default_value (str): The default value to fill in the grid (e.g., "UNUSED").

    Returns:
        numpy.ndarray: A 2D NumPy array representing the generated grid, where each
                       cell is initialized with the default value.
    """
    # Create a 2D grid (rows x cols) filled with the specified default value
    return np.full((rows, cols), default_value, dtype=object)
