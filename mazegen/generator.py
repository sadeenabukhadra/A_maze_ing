"""
Generate perfect and non-perfect mazes.

This module provides the Generator class and the functions required
to build a maze using iterative recursive backtracking and to create
optional loops for non-perfect mazes.
"""

import random
from .cell import Cell
from typing import Optional


class Generator:
    """Generate and manage the maze creation process."""

    def __init__(
        self,
        entry: tuple[int, int],
        exit_maze: tuple[int, int],
        width: int,
        height: int,
        seed: Optional[int],
    ) -> None:
        """Generate and manage the maze creation process."""
        self.entry: tuple[int, int] = entry
        self.exit_maze: tuple[int, int] = exit_maze
        self.width: int = width
        self.height: int = height
        self.seed: Optional[int] = seed
        self.grid: list[list[Cell]] = []
        self.reserved_cells: set[tuple[int, int]] = set()

    def create_grid(self) -> None:
        """Create a grid of cells with all walls initially closed."""
        for h in range(0, self.height):
            row = []
            for w in range(0, self.width):
                row.append(Cell(w, h))
            self.grid.append(row)

    def reserve_42_cells(self) -> None:
        """Reserve the cells used to draw the 42 pattern."""
        pattern: list[list[int]] = [
            [1, 0, 0, 0, 0, 1, 1, 1, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 0],
        ]
        pattern_height: int = len(pattern)
        pattern_width: int = len(pattern[0])
        start_x: int = (self.width - pattern_width) // 2
        start_y: int = (self.height - pattern_height) // 2

        for py in range(pattern_height):
            for px in range(pattern_width):
                if pattern[py][px] == 1:
                    real_x: int = start_x + px
                    real_y: int = start_y + py
                    self.reserved_cells.add((real_x, real_y))

    def choose_entry(self) -> None:
        """Validate and open the maze entry."""
        x, y = self.entry

        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError("Invalid entry coordinates: out of maze bounds.")

        if not (x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1):
            raise ValueError("Entry coordinates must be on the edges of the maze.")

        entry_cell = self.grid[y][x]

        if x == 0:
            entry_cell.open_wall("west")
        elif x == self.width - 1:
            entry_cell.open_wall("east")
        elif y == 0:
            entry_cell.open_wall("north")
        elif y == self.height - 1:
            entry_cell.open_wall("south")

    def choose_exit(self) -> None:
        """Validate and open the maze exit."""
        x, y = self.exit_maze

        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError("Invalid exit coordinates: out of maze bounds.")

        if not (x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1):
            raise ValueError("Exit coordinates must be on the edges of the maze.")

        exit_cell = self.grid[y][x]

        if x == 0:
            exit_cell.open_wall("west")
        elif x == self.width - 1:
            exit_cell.open_wall("east")
        elif y == 0:
            exit_cell.open_wall("north")
        elif y == self.height - 1:
            exit_cell.open_wall("south")

    def get_valid_neighbors(self, cell: Cell) -> list[Cell]:
        """Return all unvisited neighboring cells that can be visited."""
        x: int = cell.x
        y: int = cell.y

        possible_neighbors: list[tuple[int, int]] = [
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y),
        ]

        valid_neighbors: list[Cell] = []

        for nx, ny in possible_neighbors:
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            if (nx, ny) in self.reserved_cells:
                continue

            neighbor_cell = self.grid[ny][nx]

            if neighbor_cell.is_visited():
                continue

            valid_neighbors.append(neighbor_cell)

        return valid_neighbors

    def choose_random_neighbor(self, neighbors: list[Cell]) -> Cell:
        """Select a random neighboring cell."""
        return random.choice(neighbors)

    def remove_wall_between(self, current: Cell, neighbor: Cell) -> None:
        """Open the wall shared by two adjacent cells."""
        dx = neighbor.x - current.x
        dy = neighbor.y - current.y

        if dx == 1:
            current.open_wall("east")
            neighbor.open_wall("west")
        elif dx == -1:
            current.open_wall("west")
            neighbor.open_wall("east")
        elif dy == 1:
            current.open_wall("south")
            neighbor.open_wall("north")
        elif dy == -1:
            current.open_wall("north")
            neighbor.open_wall("south")

    def run_backtracking(self) -> None:
        """Generate a perfect maze using iterative stack backtracking."""
        x, y = self.entry
        start_cell = self.grid[y][x]
        start_cell.mark_visited()

        stack: list[Cell] = []
        stack.append(start_cell)

        while stack:
            current = stack[-1]
            neighbors = self.get_valid_neighbors(current)

            if neighbors:
                chosen_neighbor = self.choose_random_neighbor(neighbors)
                self.remove_wall_between(current, chosen_neighbor)
                chosen_neighbor.mark_visited()
                stack.append(chosen_neighbor)
            else:
                stack.pop()

    def closed_neighbors(self, cell: Cell) -> list[Cell]:
        """Return neighboring cells separated by a closed wall."""
        x: int = cell.x
        y: int = cell.y

        possible = [
            (x, y - 1, "north"),
            (x, y + 1, "south"),
            (x - 1, y, "west"),
            (x + 1, y, "east"),
        ]

        closed_neighbors: list[Cell] = []

        for nx, ny, direction in possible:
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if (nx, ny) in self.reserved_cells:
                continue
            if cell.status_wall(direction):
                closed_neighbors.append(self.grid[ny][nx])

        return closed_neighbors

    def is_open_area(self, top_x: int, top_y: int) -> bool:
        """Check whether a 3×3 area is completely open."""
        for dy in range(3):
            for dx in range(3):
                cx, cy = top_x + dx, top_y + dy
                cell = self.grid[cy][cx]

                if dx < 2 and cell.status_wall("east"):
                    return False
                if dy < 2 and cell.status_wall("south"):
                    return False
        return True

    def can_open_wall(self, a: Cell, b: Cell) -> bool:
        """Determine whether opening a wall is allowed."""
        min_x = min(a.x, b.x)
        max_x = max(a.x, b.x)
        min_y = min(a.y, b.y)
        max_y = max(a.y, b.y)

        for top_y in range(max_y - 2, min_y + 1):
            if top_y < 0 or top_y + 2 >= self.height:
                continue
            for top_x in range(max_x - 2, min_x + 1):
                if top_x < 0 or top_x + 2 >= self.width:
                    continue
                if self.is_open_area(top_x, top_y):
                    return True
        return False


def add_loop(generator: Generator) -> None:
    """Add random loops to the generated maze."""
    attempts = (generator.width * generator.height) // 10
    if attempts == 0:
        attempts += 1
    for _ in range(attempts):
        x = random.randint(0, generator.width - 1)
        y = random.randint(0, generator.height - 1)

        if (x, y) in generator.reserved_cells:
            continue

        curr = generator.grid[y][x]
        close_neighbors = generator.closed_neighbors(curr)

        if not close_neighbors:
            continue

        neighbor = random.choice(close_neighbors)

        if generator.can_open_wall(curr, neighbor):
            continue

        generator.remove_wall_between(curr, neighbor)


def perfect(generator: Generator) -> list[list[Cell]]:
    """Generate and return a perfect maze."""
    if generator.seed is not None:
        random.seed(generator.seed)

    generator.create_grid()
    if generator.height >= 7 or generator.width >= 11:
        generator.reserve_42_cells()
    else:
        print("The maze is very small")
    generator.choose_entry()
    generator.choose_exit()
    generator.run_backtracking()
    return generator.grid


def none_perfect(generator: Generator) -> list[list[Cell]]:
    """Generate and return a non-perfect maze."""
    if generator.seed is not None:
        random.seed(generator.seed)

    generator.create_grid()
    if generator.height >= 7 or generator.width >= 11:
        generator.reserve_42_cells()
    else:
        print("The maze is very small")
    generator.choose_entry()
    generator.choose_exit()
    generator.run_backtracking()
    add_loop(generator)
    return generator.grid
