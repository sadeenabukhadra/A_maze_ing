from .cell import Cell


# to know the neighbors
class Maze:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows: int = rows
        self.cols: int = cols

        self.cells: dict[tuple[int, int], Cell] = {}

        self.create_cells()

    def create_cells(self) -> None:
        for y in range(self.rows):
            for x in range(self.cols):
                self.cells[(x, y)] = Cell(x, y)

    def get_cell(self, position: tuple[int, int]) -> Cell:
        return self.cells[position]
