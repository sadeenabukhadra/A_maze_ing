from mazegen.generator import Generator, perfect
from mazegen.solver import MazeSolver


WIDTH = 14
HEIGHT = 15
ENTRY = (0, 0)
EXIT = (WIDTH - 1, HEIGHT - 1)


def make_maze() -> Generator:
    generator = Generator(
        entry=ENTRY,
        exit_maze=EXIT,
        width=WIDTH,
        height=HEIGHT,
        seed=42,
    )

    perfect(generator)

    return generator


def test_solver_finds_solution() -> None:
    generator = make_maze()

    solver = MazeSolver(ENTRY, EXIT)

    solution = solver.solve(generator)

    assert solution is not None
    assert len(solution) > 0


def test_solution_starts_at_entry() -> None:
    generator = make_maze()

    solver = MazeSolver(ENTRY, EXIT)

    solution = solver.solve(generator)

    assert solution is not None
    assert solution[0] == ENTRY


def test_solution_ends_at_exit() -> None:
    generator = make_maze()

    solver = MazeSolver(ENTRY, EXIT)

    solution = solver.solve(generator)

    assert solution is not None
    assert solution[-1] == EXIT


def test_solution_coordinates_are_inside_maze() -> None:
    generator = make_maze()

    solver = MazeSolver(ENTRY, EXIT)

    solution = solver.solve(generator)

    assert solution is not None

    for x, y in solution:
        assert 0 <= x < WIDTH
        assert 0 <= y < HEIGHT
