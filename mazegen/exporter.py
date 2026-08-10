"""
Export maze into hexadecimal format.

Each cell is represented by one hexadecimal digit.
The digit encodes the closed walls:
    Bit 0 -> North
    Bit 1 -> East
    Bit 2 -> South
    Bit 3 -> West

After the grid, the file also contains (separated by a blank line):
    1. The entry coordinates ("x,y")
    2. The exit coordinates ("x,y")
    3. The shortest path from entry to exit, as a string of N/E/S/W
       letters.
"""

from .cell import Cell

# Maps a (dx, dy) displacement between two adjacent cells to the
# direction letter required by the output file format.
_STEP_TO_LETTER: dict[tuple[int, int], str] = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W",
}


class MazeExporter:
    """
    Export a generated maze into a file.
    """

    def __init__(self, grid: list[list[Cell]]) -> None:
        """
        Initialize the exporter.

        Args:
            grid: The maze grid containing Cell objects.
        """
        self.grid: list[list[Cell]] = grid

    def cell_to_hex(self, cell: Cell) -> str:
        """
        Convert a single cell wall configuration into hexadecimal.

        Args:
            cell: A maze cell.

        Returns:
            A hexadecimal character representing the cell walls.
        """

        value: int = 0

        # Bit 0: North
        if cell.north:
            value |= 1

        # Bit 1: East
        if cell.east:
            value |= 2

        # Bit 2: South
        if cell.south:
            value |= 4

        # Bit 3: West
        if cell.west:
            value |= 8

        return format(value, "X")

    def path_to_letters(
        self, path: list[tuple[int, int]]
    ) -> str:
        """
        Convert a path of coordinates into a string of N/E/S/W letters.

        Args:
            path: Ordered list of (x, y) coordinates from entry to
                exit, as produced by MazeSolver.solve().

        Returns:
            The path expressed as consecutive direction letters, e.g.
            "SWSESW". Returns an empty string for a path of 0 or 1
            cells.

        Raises:
            ValueError: If two consecutive coordinates in the path
                are not orthogonally adjacent (i.e. not a valid
                single step).
        """
        letters: str = ""

        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            step = (x2 - x1, y2 - y1)

            if step not in _STEP_TO_LETTER:
                raise ValueError(
                    f"Invalid path step from ({x1},{y1}) to ({x2},{y2})"
                )

            letters += _STEP_TO_LETTER[step]

        return letters

    def export(
        self,
        filename: str,
        entry: tuple[int, int],
        exit_maze: tuple[int, int],
        solution: list[tuple[int, int]],
    ) -> None:
        """
        Export the maze into a hexadecimal text file.

        Writes the hex-encoded grid, then a blank line, then the
        entry coordinates, exit coordinates, and shortest path
        (N/E/S/W), as required by the output file format.

        Args:
            filename: Output file name.
            entry: (x, y) coordinates of the entry cell.
            exit_maze: (x, y) coordinates of the exit cell.
            solution: Shortest path from entry to exit, as a list of
                (x, y) coordinates (e.g. the result of
                MazeSolver.solve()).
        """
        path_letters = self.path_to_letters(solution)

        with open(filename, "w") as file:

            for row in self.grid:

                line: str = ""

                for cell in row:
                    line += self.cell_to_hex(cell)

                file.write(line + "\n")

            file.write("\n")
            file.write(f"{entry[0]},{entry[1]}\n")
            file.write(f"{exit_maze[0]},{exit_maze[1]}\n")
            file.write(f"{path_letters}\n")
