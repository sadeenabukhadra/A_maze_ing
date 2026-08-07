from solver import MazeSolver


class FakeMaze:
    """Simple maze used to test the BFS solver."""

    def __init__(self) -> None:
        self.graph = {
            (0, 0): [(1, 0), (0, 1)],
            (1, 0): [(0, 0), (2, 0)],
            (2, 0): [(1, 0), (2, 1)],
            (2, 1): [(2, 0), (2, 2)],
            (2, 2): [(2, 1), (1, 2)],
            (1, 2): [(2, 2), (0, 2)],
            (0, 2): [(1, 2), (0, 1)],
            (0, 1): [(0, 0), (0, 2)],
        }

    def get_neighbors(self, current: tuple[int, int]) -> list[tuple[int, int]]:
        return self.graph.get(current, [])


def main() -> None:
    maze = FakeMaze()

    solver = MazeSolver(
        start=(0, 0),
        end=(2, 2),
    )

    path = solver.solve(maze)

    print("========== Solver Test ==========")

    if path is None:
        print("✗ No path found")
        return

    print("✓ Path found")
    print("Path:", path)

    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)

    print("✓ Start is correct")
    print("✓ End is correct")
    print("✓ BFS test passed")


if __name__ == "__main__":
    main()
