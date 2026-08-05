from collections import deque
from typing import Deque
from .cell import Cell
from .generator import Generator


class MazeSolver:
    """
    Solves a maze using the Breadth-First Search (BFS) algorithm.
    """

    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> None:
        """
        Initialize the maze solver.

        Args:
            start: Starting cell coordinates.
            end: Target cell coordinates.
        """

        self.start: tuple[int, int] = start
        self.end: tuple[int, int] = end

        self.queue: Deque[tuple[int, int]] = deque()

        self.visited: set[tuple[int, int]] = set()

        self.parent: dict[
            tuple[int, int],
            tuple[int, int]
        ] = {}

<<<<<<< HEAD
    def solve(
        self,
        maze: Generator
    ) -> list[tuple[int, int]] | None:
=======
    def get_open_neighbors(self,
                           current: tuple[int, int],
                           maze: Generator
                           ) -> list[tuple[int, int]]:
        """
        Return neighboring coordinates reachable through an open wall.
 
        This does not rely on any Generator-specific method beyond its
        public attributes (grid, width, height) and Cell.status_wall,
        so it works with Generator exactly as it is, without any
        modification to generator.py.
        """
        x, y = current
        curr_cell = maze.grid[y][x]

        directions = [
            (0, -1, "north"),
            (0, 1, "south"),
            (-1, 0, "west"),
            (1, 0, "east")
        ]

        open_neigh = []

        for dx, dy, direction in directions:
            nx, ny = x + dx, y + dy

            if not(0 <= nx < maze.width and 0 <= ny < maze.height):
                continue

            if not curr_cell.status_wall(direction):
                open_neigh.append((nx, ny))

        return open_neigh

    def solve(self, maze: Generator) -> list[tuple[int, int]] | None:
>>>>>>> origin/main
        """
        Find a path from start to end using BFS.

        Args:
            maze: Generated maze.

        Returns:
            Shortest path as coordinates or None.
        """

        self.queue.append(self.start)
        self.visited.add(self.start)

        while self.queue:

            current: tuple[int, int] = self.queue.popleft()

            if current == self.end:
                return self.reconstruct_path()

<<<<<<< HEAD
            x, y = current

            current_cell: Cell = maze.grid[y][x]

            neighbors: list[Cell] = (
                maze.get_valid_neighbors(current_cell)
=======
            # Ask Maze for possible moves
            neighbors: list[tuple[int, int]] = maze.get_open_neighbors(
                current, maze
>>>>>>> origin/main
            )

            for neighbor in neighbors:

                position: tuple[int, int] = (
                    neighbor.x,
                    neighbor.y
                )

                if position not in self.visited:

                    self.visited.add(position)

                    self.parent[position] = current

                    self.queue.append(position)

        return None

    def reconstruct_path(self) -> list[tuple[int, int]]:
        """
        Rebuild the path after reaching the end.

        Returns:
            Path from start to end.
        """

        path: list[tuple[int, int]] = []

        current: tuple[int, int] = self.end

        while current != self.start:

            path.append(current)

            current = self.parent[current]

        path.append(self.start)

        path.reverse()

        return path

