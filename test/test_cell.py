from mazegen.cell import Cell


def test_cell_coordinates() -> None:
    cell = Cell(3, 5)

    assert cell.x == 3
    assert cell.y == 5


def test_new_cell_is_not_visited() -> None:
    cell = Cell(0, 0)

    assert not cell.is_visited()


def test_mark_visited() -> None:
    cell = Cell(0, 0)

    cell.mark_visited()

    assert cell.is_visited()


def test_open_north_wall() -> None:
    cell = Cell(0, 0)

    cell.open_wall("north")

    assert not cell.north


def test_open_south_wall() -> None:
    cell = Cell(0, 0)

    cell.open_wall("south")

    assert not cell.south


def test_open_east_wall() -> None:
    cell = Cell(0, 0)

    cell.open_wall("east")

    assert not cell.east


def test_open_west_wall() -> None:
    cell = Cell(0, 0)

    cell.open_wall("west")

    assert not cell.west


def test_status_wall() -> None:
    cell = Cell(0, 0)

    assert cell.status_wall("north")
    assert cell.status_wall("south")
    assert cell.status_wall("east")
    assert cell.status_wall("west")

    cell.open_wall("north")

    assert not cell.status_wall("north")
