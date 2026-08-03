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

    def solve(
        self,
        maze: Generator
    ) -> list[tuple[int, int]] | None:
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

            x, y = current

            current_cell: Cell = maze.grid[y][x]

            neighbors: list[Cell] = (
                maze.get_valid_neighbors(current_cell)
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
