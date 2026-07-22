class Cell:
    """
    Represents a single cell in the maze.

    Each cell stores its position, visitation state, and the status
    of its four surrounding walls (north, east, south, and west).
    """
    def __init__(self, x: int, y: int) -> None:
        """
        Initialize a new cell.

        Args:
            x: Horizontal position of the cell.
            y: Vertical position of the cell.
        """
        self.x: int = x
        self.y: int = y
        self.visited: bool = False
        self.north: bool = True
        self.east: bool = True
        self.west: bool = True
        self.south: bool = True

    def is_visited(self) -> bool:
        """
        Check whether the cell has been visited.

        Returns:
            True if the cell has been visited, otherwise False.
        """
        return self.visited

    def mark_visited(self) -> None:
        """
        Mark the cell as visited.
        """
        self.visited = True

    def status_wall(self, direction: str) -> bool:
        """
        Return the status of a wall.

        Args:
            direction: One of "north", "east", "south", or "west".

        Returns:
            True if the wall is closed, False if it is open.

        Raises:
            ValueError: If the direction is invalid.
        """
        if direction == "north":
            return self.north
        elif direction == "south":
            return self.south
        elif direction == "west":
            return self.west
        elif direction == "east":
            return self.east
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def open_wall(self, direction: str) -> None:
        """
        Open the specified wall.

        Args:
            direction: One of "north", "east", "south", or "west".

        Raises:
            ValueError: If the direction is invalid.
        """
        if direction == "north":
            self.north = False
        elif direction == "south":
            self.south = False
        elif direction == "west":
            self.west = False
        elif direction == "east":
            self.east = False
        else:
            raise ValueError(f"Invalid direction: {direction}")
