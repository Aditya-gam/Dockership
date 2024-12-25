# Dockership/tasks/balancing.py

import copy  # For deep copying ship grids
import re  # For parsing and handling manifest file strings
import numpy as np  # For numerical operations (not used directly here)
from collections.abc import Iterable  # For type checking iterables

# Class to represent a container


class Container:
    def __init__(self, name, weight):
        """
        Initialize a container with a name and weight.

        Args:
            name (str): Name of the container.
            weight (int): Weight of the container.
        """
        self.name = name
        self.weight = weight


# Class to represent a slot in the ship grid
class Slot:
    def __init__(self, container: Container, has_container, available):
        """
        Initialize a slot with container details, availability, and status.

        Args:
            container (Container or None): Container in the slot (if any).
            has_container (bool): Indicates if the slot contains a container.
            available (bool): Indicates if the slot is available for new containers.
        """
        self.container = container
        self.has_container = has_container
        self.available = available


# Function to create an empty ship grid
def create_ship_grid(rows, columns):
    """
    Creates an empty ship grid with the specified dimensions.

    Args:
        rows (int): Number of rows in the grid.
        columns (int): Number of columns in the grid.

    Returns:
        list[list[Slot]]: A grid filled with empty slots.
    """
    return [[Slot(None, False, False) for _ in range(columns)] for _ in range(rows)]


# Function to update the ship grid based on manifest data
def update_ship_grid(file_content, ship_grid, containers):
    """
    Updates the ship grid with data from the manifest file.

    Args:
        file_content (str): Manifest file content.
        ship_grid (list[list[Slot]]): The ship grid to update.
        containers (list): List to store container locations.
    """
    for line in file_content.splitlines():
        slot_data = line.split()
        loc = [int(val) - 1 for val in re.sub(r"[\[\]]", '',
                                              slot_data[0]).split(",")[:2]]  # Extract location
        weight = int(re.sub(r"[\{\}\,]", '', slot_data[1]))  # Extract weight
        status = slot_data[2] if len(slot_data) == 3 else " ".join(
            slot_data[2:])  # Extract status
        x, y = loc

        if 0 <= x < len(ship_grid) and 0 <= y < len(ship_grid[0]):
            if status == "NAN":
                ship_grid[x][y] = Slot(
                    None, has_container=False, available=False)
            elif status == "UNUSED":
                ship_grid[x][y] = Slot(
                    None, has_container=False, available=True)
            else:
                ship_grid[x][y] = Slot(
                    Container(status, weight), has_container=True, available=False)
                containers.append(loc)


# Function to calculate weight balance between the ship's left and right sides
def calculate_balance(ship_grid):
    """
    Calculates the left and right weight balance of the ship.

    Args:
        ship_grid (list[list[Slot]]): The ship grid.

    Returns:
        tuple: Left weight, right weight, and whether the ship is balanced.
    """
    left_balance, right_balance = 0, 0
    halfway = len(ship_grid[0]) // 2

    for row in ship_grid:
        for idx, slot in enumerate(row):
            if slot.container:
                if idx < halfway:
                    left_balance += slot.container.weight
                else:
                    right_balance += slot.container.weight

    balanced = 0.9 <= left_balance / \
        right_balance <= 1.1 if right_balance > 0 else False
    return left_balance, right_balance, balanced


# Function to balance the ship by moving containers
def balance(ship_grid, containers):
    """
    Balances the ship by moving containers between sides.

    Args:
        ship_grid (list[list[Slot]]): The ship grid.
        containers (list): List of container locations.

    Returns:
        tuple: Steps taken, ship grid snapshots, and balance status.
    """
    steps, ship_grids = [], []
    left_balance, right_balance, balanced = calculate_balance(ship_grid)
    max_iterations = 100  # Prevent infinite loops

    while not balanced and max_iterations > 0:
        # Identify containers on the heavier side
        side_containers = [
            loc for loc in containers if (loc[1] < len(ship_grid[0]) // 2) == (left_balance > right_balance)
        ]

        if not side_containers:
            break

        # Select a container to move
        container_to_move = side_containers[0]
        # Find the nearest available slot on the lighter side
        goal_loc = nearest_available_balance(
            left_balance, right_balance, ship_grid)

        if goal_loc == (-1, -1):  # No valid slot found
            break

        # Move the container and update the grid
        step, updated_grid = move_to(container_to_move, goal_loc, ship_grid)
        steps.append(step)
        ship_grids.append(updated_grid)

        containers.remove(container_to_move)
        containers.append(goal_loc)
        left_balance, right_balance, balanced = calculate_balance(ship_grid)
        max_iterations -= 1

    return steps, ship_grids, balanced


# Function to move a container to a new location
def move_to(container_loc, goal_loc, ship_grid):
    """
    Moves a container to a new location in the ship grid.

    Args:
        container_loc (tuple): Current location of the container.
        goal_loc (tuple): Target location for the container.
        ship_grid (list[list[Slot]]): The ship grid.

    Returns:
        tuple: Step description and updated grid snapshot.
    """
    x1, y1 = container_loc
    x2, y2 = goal_loc
    ship_grid[x2][y2].container = ship_grid[x1][y1].container
    ship_grid[x2][y2].has_container = True
    ship_grid[x2][y2].available = False
    ship_grid[x1][y1].container = None
    ship_grid[x1][y1].has_container = False
    ship_grid[x1][y1].available = True

    return f"Moved container from {container_loc} to {goal_loc}", copy.deepcopy(ship_grid)


# Function to find the nearest available slot on the lighter side
def nearest_available_balance(left_balance, right_balance, ship_grid):
    """
    Finds the nearest available slot on the lighter side of the ship.

    Args:
        left_balance (int): Weight on the left side of the ship.
        right_balance (int): Weight on the right side of the ship.
        ship_grid (list[list[Slot]]): The ship grid.

    Returns:
        tuple: Coordinates of the nearest available slot or (-1, -1) if none found.
    """
    halfway = len(ship_grid[0]) // 2
    side = range(halfway, len(
        ship_grid[0])) if left_balance > right_balance else range(halfway)

    for row_idx, row in enumerate(ship_grid):
        for col_idx in side:
            if row[col_idx].available and (row_idx == 0 or not ship_grid[row_idx - 1][col_idx].available):
                return row_idx, col_idx
    return -1, -1
