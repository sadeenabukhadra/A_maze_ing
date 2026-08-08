from mazegen.generator import Generator, perfect
from mazegen.renderer import Color, RendererMaze


WIDTH = 14
HEIGHT = 15
ENTRY = (0, 0)
EXIT = (WIDTH - 1, HEIGHT - 1)


def make_renderer() -> RendererMaze:
    generator = Generator(
        entry=ENTRY,
        exit_maze=EXIT,
        width=WIDTH,
        height=HEIGHT,
        seed=42,
    )

    perfect(generator)

    return RendererMaze(generator)


def test_renderer_initial_state() -> None:
    renderer = make_renderer()

    assert renderer.generator is not None
    assert renderer.solution is None
    assert renderer.show_solution is False


def test_get_content_entry() -> None:
    renderer = make_renderer()

    content = renderer.get_content(*ENTRY)

    assert "●" in content


def test_get_content_exit() -> None:
    renderer = make_renderer()

    content = renderer.get_content(*EXIT)

    assert "■" in content


def test_get_content_empty_cell() -> None:
    renderer = make_renderer()

    content = renderer.get_content(5, 5)

    assert isinstance(content, str)


def test_get_directions() -> None:
    renderer = make_renderer()

    directions = renderer.get_directions(0, 0)

    assert len(directions) == 4
    assert all(isinstance(value, bool) for value in directions)


def test_get_junction() -> None:
    renderer = make_renderer()

    junction = renderer.get_junction(0, 0)

    assert isinstance(junction, str)
    assert len(junction) == 1


def test_toggle_solution() -> None:
    renderer = make_renderer()

    assert renderer.show_solution is False

    renderer.toggle_solution()

    assert renderer.show_solution is True

    renderer.toggle_solution()

    assert renderer.show_solution is False


def test_change_color() -> None:
    renderer = make_renderer()

    initial_index = renderer.curr_color_index

    renderer.change_color()

    assert renderer.curr_color_index != initial_index
    assert isinstance(renderer.curr_color, Color)


def test_change_color_cycles() -> None:
    renderer = make_renderer()

    number_of_colors = len(renderer.colors)
    initial_index = renderer.curr_color_index

    for _ in range(number_of_colors):
        renderer.change_color()

    assert renderer.curr_color_index == initial_index


def test_has_vwall() -> None:
    renderer = make_renderer()

    result = renderer.has_vwall(0, 0)

    assert isinstance(result, bool)


def test_has_hwall() -> None:
    renderer = make_renderer()

    result = renderer.has_hwall(0, 0)

    assert isinstance(result, bool)


def test_is_reserved_outside_bounds() -> None:
    renderer = make_renderer()

    assert renderer.is_reseved(-1, 0) is False
    assert renderer.is_reseved(0, -1) is False
    assert renderer.is_reseved(WIDTH, 0) is False
    assert renderer.is_reseved(0, HEIGHT) is False


def test_render(capsys) -> None:
    renderer = make_renderer()

    renderer.render()

    captured = capsys.readouterr()

    assert captured.out != ""


def test_print_menu(capsys) -> None:
    renderer = make_renderer()

    renderer.print_menu()

    captured = capsys.readouterr()

    assert "Options:" in captured.out
    assert "Re-generate new maze" in captured.out
    assert "Toggle solution path" in captured.out
    assert "Change wall color" in captured.out
    assert "Quit" in captured.out
