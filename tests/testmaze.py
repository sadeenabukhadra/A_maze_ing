"""from generator import Generator, perfect


def main() -> None:
    generator = Generator(
        entry=(0, 0),
        exit_maze=(1,2),
        width=3,
        height=3,
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
    """



"""
ملف اختبار مؤقت بس - يطبع المتاهة بشكل ASCII واضح بالـ terminal
S = نقطة الدخول (Entry) | E = نقطة الخروج (Exit)
هذا مو renderer.py الرسمي، هذا بس أداة فحص بصري سريعة.
"""
from cell import Cell
from generator import Generator, perfect, none_perfect


def print_maze(
    grid: list[list[Cell]],
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_point: tuple[int, int],
) -> None:
    # الصف العلوي بالكامل (جدران شمالية لأول صف)
    top = "+"
    for x in range(width):
        top += "---+" if grid[0][x].status_wall("north") else "   +"
    print(top)

    for y in range(height):
        # سطر الخلايا: الجدار الغربي + محتوى الخلية (فاضي أو S/E)
        row = ""
        for x in range(width):
            cell = grid[y][x]
            left_wall = "|" if cell.status_wall("west") else " "

            if (x, y) == entry:
                content = " S "
            elif (x, y) == exit_point:
                content = " E "
            else:
                content = "   "

            row += left_wall + content

        row += "|" if grid[y][width - 1].status_wall("east") else " "
        print(row)

        # سطر الجدران الجنوبية لهذا الصف
        bottom = "+"
        for x in range(width):
            cell = grid[y][x]
            bottom += "---+" if cell.status_wall("south") else "   +"
        print(bottom)


if __name__ == "__main__":
    WIDTH = 3
    HEIGHT = 3
    ENTRY = (0, 0)
    EXIT = (WIDTH - 1, HEIGHT - 1)
    SEED = 42

    print("=" * 65)
    print("PERFECT MAZE   (S = Entry, E = Exit)")
    print("=" * 65)
    gen1 = Generator(ENTRY, EXIT, WIDTH, HEIGHT, SEED)
    maze1 = perfect(gen1)
    print_maze(maze1, WIDTH, HEIGHT, ENTRY, EXIT)

    print()
    print("=" * 65)
    print("NONE PERFECT MAZE (Pac-Man style, with loops)")
    print("=" * 65)
    gen2 = Generator(ENTRY, EXIT, WIDTH, HEIGHT, SEED)
    maze2 = none_perfect(gen2)
    print_maze(maze2, WIDTH, HEIGHT, ENTRY, EXIT)
