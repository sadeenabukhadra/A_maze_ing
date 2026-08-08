import pytest

from mazegen.generator import Generator, perfect, none_perfect


WIDTH = 14
HEIGHT = 15
ENTRY = (0, 0)
EXIT = (WIDTH - 1, HEIGHT - 1)


def make_generator(seed: int | None = 42) -> Generator:
    return Generator(
        entry=ENTRY,
        exit_maze=EXIT,
        width=WIDTH,
        height=HEIGHT,
        seed=seed,
    )


def test_generator_initial_state() -> None:
    generator = make_generator()

    assert generator.entry == ENTRY
    assert generator.exit_maze == EXIT
    assert generator.width == WIDTH
    assert generator.height == HEIGHT
    assert generator.seed == 42
    assert generator.grid == []
    assert generator.reserved_cells == set()


def test_create_grid() -> None:
    generator = make_generator()

    generator.create_grid()

    assert len(generator.grid) == HEIGHT
    assert all(len(row) == WIDTH for row in generator.grid)


def test_create_grid_contains_correct_coordinates() -> None:
    generator = make_generator()

    generator.create_grid()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            cell = generator.grid[y][x]

            assert cell.x == x
            assert cell.y == y


def test_reserve_42_cells() -> None:
    generator = make_generator()

    generator.create_grid()
    generator.reserve_42_cells()

    assert len(generator.reserved_cells) > 0


def test_reserved_cells_are_inside_grid() -> None:
    generator = make_generator()

    generator.create_grid()
    generator.reserve_42_cells()

    for x, y in generator.reserved_cells:
        assert 0 <= x < WIDTH
        assert 0 <= y < HEIGHT


def test_choose_entry_accepts_valid_entry() -> None:
    generator = make_generator()

    generator.create_grid()
    generator.choose_entry()


def test_choose_exit_accepts_valid_exit() -> None:
    generator = make_generator()

    generator.create_grid()
    generator.choose_exit()


@pytest.mark.parametrize(
    "entry",
    [
        (-1, 0),
        (WIDTH, 0),
        (0, -1),
        (0, HEIGHT),
        (5, 5),
    ],
)
def test_choose_entry_rejects_invalid_entry(
    entry: tuple[int, int],
) -> None:
    generator = Generator(
        entry=entry,
        exit_maze=EXIT,
        width=WIDTH,
        height=HEIGHT,
        seed=42,
    )

    generator.create_grid()

    with pytest.raises(ValueError):
        generator.choose_entry()


@pytest.mark.parametrize(
    "exit_maze",
    [
        (-1, 0),
        (WIDTH, 0),
        (0, -1),
        (0, HEIGHT),
        (5, 5),
    ],
)
def test_choose_exit_rejects_invalid_exit(
    exit_maze: tuple[int, int],
) -> None:
    generator = Generator(
        entry=ENTRY,
        exit_maze=exit_maze,
        width=WIDTH,
        height=HEIGHT,
        seed=42,
    )

    generator.create_grid()

    with pytest.raises(ValueError):
        generator.choose_exit()


def test_get_valid_neighbors_excludes_out_of_bounds() -> None:
    generator = make_generator()

    generator.create_grid()

    cell = generator.grid[0][0]
    neighbors = generator.get_valid_neighbors(cell)

    for neighbor in neighbors:
        assert 0 <= neighbor.x < WIDTH
        assert 0 <= neighbor.y < HEIGHT


def test_get_valid_neighbors_excludes_reserved_cells() -> None:
    generator = make_generator()

    generator.create_grid()
    generator.reserve_42_cells()

    for x, y in generator.reserved_cells:
        cell = generator.grid[y][x]

        if cell.is_visited():
            continue

        neighbors = generator.get_valid_neighbors(cell)

        assert all(
            (neighbor.x, neighbor.y)
            not in generator.reserved_cells
            for neighbor in neighbors
        )


def test_choose_random_neighbor() -> None:
    generator = make_generator()

    generator.create_grid()

    cell = generator.grid[0][0]
    neighbors = generator.get_valid_neighbors(cell)

    if neighbors:
        selected = generator.choose_random_neighbor(neighbors)

        assert selected in neighbors


def test_remove_wall_between_horizontal_cells() -> None:
    generator = make_generator()

    generator.create_grid()

    current = generator.grid[0][0]
    neighbor = generator.grid[0][1]

    generator.remove_wall_between(current, neighbor)

    assert current.east is False
    assert neighbor.west is False


def test_remove_wall_between_vertical_cells() -> None:
    generator = make_generator()

    generator.create_grid()

    current = generator.grid[0][0]
    neighbor = generator.grid[1][0]

    generator.remove_wall_between(current, neighbor)

    assert current.south is False
    assert neighbor.north is False


def test_run_backtracking_visits_cells() -> None:
    generator = make_generator()

    generator.create_grid()
    generator.run_backtracking()

    visited = [
        cell
        for row in generator.grid
        for cell in row
        if cell.is_visited()
    ]

    assert len(visited) > 0


def test_perfect_generates_grid() -> None:
    generator = make_generator()

    result = perfect(generator)

    assert result == generator.grid
    assert len(result) == HEIGHT
    assert len(result[0]) == WIDTH


def test_none_perfect_generates_grid() -> None:
    generator = make_generator()

    result = none_perfect(generator)

    assert result == generator.grid
    assert len(result) == HEIGHT
    assert len(result[0]) == WIDTH


def test_seed_produces_deterministic_perfect_maze() -> None:
    generator1 = make_generator(42)
    generator2 = make_generator(42)

    perfect(generator1)
    perfect(generator2)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            cell1 = generator1.grid[y][x]
            cell2 = generator2.grid[y][x]

            assert cell1.north == cell2.north
            assert cell1.south == cell2.south
            assert cell1.east == cell2.east
            assert cell1.west == cell2.west


def test_different_seeds_can_generate_different_mazes() -> None:
    generator1 = make_generator(42)
    generator2 = make_generator(123)

    perfect(generator1)
    perfect(generator2)

    walls1 = [
        (
            cell.north,
            cell.south,
            cell.east,
            cell.west,
        )
        for row in generator1.grid
        for cell in row
    ]

    walls2 = [
        (
            cell.north,
            cell.south,
            cell.east,
            cell.west,
        )
        for row in generator2.grid
        for cell in row
    ]

    assert walls1 != walls2
