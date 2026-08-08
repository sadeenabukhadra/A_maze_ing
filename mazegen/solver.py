from collections import deque
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

        self.queue: deque[tuple[int, int]] = deque()

        self.visited: set[tuple[int, int]] = set()

        # Stores where each cell came from
        self.parent: dict[tuple[int, int], tuple[int, int]] = {}

    def get_open_neighbors(
            self,
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

            if not (0 <= nx < maze.width and 0 <= ny < maze.height):
                continue

            if not curr_cell.status_wall(direction):
                open_neigh.append((nx, ny))

        return open_neigh

    def solve(self, maze: Generator) -> list[tuple[int, int]] | None:
        """
        Find a path from start to end using BFS.

        Args:
            maze: Maze object that provides accessible neighbors.

        Returns:
            The shortest path as a list of coordinates,
            or None if no path exists.
        """
        self.queue.append(self.start)
        self.visited.add(self.start)

        while self.queue:

            current: tuple[int, int] = self.queue.popleft()

            # Goal reached
            if current == self.end:
                return self.reconstruct_path()

            # Ask Maze for possible moves
            neighbors: list[tuple[int, int]] = self.get_open_neighbors(
                current, maze
            )

            for neighbor in neighbors:

                if neighbor not in self.visited:

                    # Mark as discovered
                    self.visited.add(neighbor)

                    # Remember the previous cell
                    self.parent[neighbor] = current

                    # Add to BFS queue
                    self.queue.append(neighbor)

        return None

    def reconstruct_path(self) -> list[tuple[int, int]]:
        """
        Rebuild the path after reaching the end.

        Returns:
            List of coordinates from start to end.
        """

        path: list[tuple[int, int]] = []

        current: tuple[int, int] = self.end

        while current != self.start:

            path.append(current)

            current = self.parent[current]

        # Add starting point
        path.append(self.start)

        # Reverse because we built it backwards
        path.reverse()

        return path
