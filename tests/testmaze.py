"""
from generator import Generator, perfect


def main() -> None:
    generator = Generator(
        entry=(0, 0),
        exit_maze=(9, 9),
        width=10,
        height=10,
        seed=42,
    )

    grid = perfect(generator)

    print("========== Generator Test ==========\n")

    print("Grid size:")
    print(f"Rows    : {len(grid)}")
    print(f"Columns : {len(grid[0])}")

    assert len(grid) == generator.height
    assert len(grid[0]) == generator.width

    print("✓ Grid created correctly\n")

    
    visited = 0

    for row in grid:
        for cell in row:
            if cell.is_visited():
                visited += 1

    print(f"Visited cells : {visited}")

    expected = (
        generator.width * generator.height
        - len(generator.reserved_cells)
    )

    if visited == expected:
        print("✓ All reachable cells visited")
    else:
        print(f"✗ Expected {expected}, got {visited}")

    x, y = generator.entry
    entry = grid[y][x]

    print("Entry walls:")
    print(
        "North:", entry.status_wall("north"),
        "South:", entry.status_wall("south"),
        "East :", entry.status_wall("east"),
        "West :", entry.status_wall("west"),
    )
    print()

    
    x, y = generator.exit_maze
    exit_cell = grid[y][x]

    print("Exit walls:")
    print(
        "North:", exit_cell.status_wall("north"),
        "South:", exit_cell.status_wall("south"),
        "East :", exit_cell.status_wall("east"),
        "West :", exit_cell.status_wall("west"),
    )
    print()

    
    print(f"Reserved cells : {len(generator.reserved_cells)}")
    print()

    print("✓ Test finished successfully")


if __name__ == "__main__":
    main()
    """

from generator import Generator, perfect


def test_wall_consistency() -> None:
    generator = Generator(
        entry=(0, 0),
        exit_maze=(9, 9),
        width=10,
        height=10,
        seed=42,
    )

    grid = perfect(generator)

    for y in range(generator.height):
        for x in range(generator.width):
            cell = grid[y][x]

            # East <-> West
            if x + 1 < generator.width:
                east = grid[y][x + 1]

                assert (
                    cell.status_wall("east")
                    == east.status_wall("west")
                ), f"Wall mismatch between ({x},{y}) and ({x+1},{y})"

            # South <-> North
            if y + 1 < generator.height:
                south = grid[y + 1][x]

                assert (
                    cell.status_wall("south")
                    == south.status_wall("north")
                ), f"Wall mismatch between ({x},{y}) and ({x},{y+1})"

    print("✓ All walls are consistent")


if __name__ == "__main__":
    test_wall_consistency()
