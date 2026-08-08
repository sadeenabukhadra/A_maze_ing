"""
Export maze into hexadecimal format.

Each cell is represented by one hexadecimal digit.
The digit encodes the closed walls:
    Bit 0 -> North
    Bit 1 -> East
    Bit 2 -> South
    Bit 3 -> West

"""

from .cell import Cell


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

    def export(self, filename: str) -> None:
        """
        Export the maze into a hexadecimal text file.

        Args:
            filename: Output file name.
        """

        with open(filename, "w") as file:

            for row in self.grid:

                line: str = ""

                for cell in row:
                    line += self.cell_to_hex(cell)

                file.write(line + "\n")
