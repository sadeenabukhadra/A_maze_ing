"""
A-Maze-ing: main entry point.

Usage:
    python3 a_maze_ing.py config.txt
"""
from parser import Parser
from mazegen.generator import Generator, perfect, none_perfect
from mazegen.solver import MazeSolver
from mazegen.renderer import RendererMaze
from mazegen.exporter import MazeExporter
import sys
from typing import Any
import shutil
import signal
import time


def install_resize_watcher(state: dict[str, bool]) -> None:
    """Install a SIGWINCH handler that flags terminal resize events.

    Args:
        state: A mutable dict used to signal a resize to the main loop
            (e.g. {"resized": False}). A dict is used instead of a
            plain bool because signal handlers cannot rebind outer
            variables directly.
    """
    def handler(signum: int, frame: Any) -> None:
        state["resized"] = True

    signal.signal(signal.SIGWINCH, handler)


def wait_for_terminal_fit(width: int, height: int) -> None:
    """Block until the terminal is large enough, printing live updates.

    Args:
        width: Maze width in cells.
        height: Maze height in cells.
    """
    need_cols = width * 4 + 1
    need_lines = height * 2 + 1

    while not check_terminal(width, height):
        print(
            "\033[2J\033[H"
            "Terminal window is too small to display this maze.\n"
            f"Required: at least {need_cols} columns x "
            f"{need_lines} lines.\n"
            "Waiting for you to enlarge the terminal...",
            flush=True
        )
        try:
            time.sleep(0.3)
        except KeyboardInterrupt:
            print("\nBye!")
            sys.exit(0)


def render_with_resize_guard(
        renderer: RendererMaze,
        state: dict[str, bool]
) -> None:
    """Render one frame, pausing automatically if the window shrank.

    Args:
        renderer: The RendererMaze instance to draw.
        state: The resize-flag dict from install_resize_watcher.
    """
    width = renderer.generator.width
    height = renderer.generator.height

    if state["resized"]:
        state["resized"] = False
        wait_for_terminal_fit(width, height)

    if not check_terminal(width, height):
        wait_for_terminal_fit(width, height)

    renderer.render()


def load_config(config_path: str) -> dict[str, Any]:
    """
    Parse the configuration file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        Parsed configuration.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the configuration is invalid.
    """
    parser = Parser(config_path)
    return parser.parse()


def bulid_generator(config: dict[str, Any]) -> Generator:
    """
        Create and run the maze generator from the parsed configuration.

        Args:
        config: Parsed configuration.

        Returns:
        A generated Generator instance.

        Raises:
        ValueError: If generation parameters are invalid.
    """
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit_maze = config["EXIT"]
    perfect_mod = config["PERFECT"]

    if not isinstance(height, int):
        raise TypeError("HEIGHT must be an intger")

    if not isinstance(width, int):
        raise TypeError("WIDTH must be an intger")

    if not isinstance(entry, tuple):
        raise TypeError("ENTRY must be a coordinte pair .")
    if not isinstance(exit_maze, tuple):
        raise TypeError("EXIT must be a coordinte pair .")
    if not isinstance(perfect_mod, bool):
        raise TypeError("PERFECT must be True or False")

    seed = config.get("SEED")
    if seed is not None and not isinstance(seed, int):
        raise ValueError("SEED must be an intger .")

    generator = Generator(
        entry=entry,
        exit_maze=exit_maze,
        width=width,
        height=height,
        seed=seed
    )

    if perfect_mod:
        perfect(generator)
    else:
        none_perfect(generator)

    return generator


def solve_maze(generator: Generator) -> list[tuple[int, int]]:
    """
    Find the shortest path from entry to exit.

    Args:
        generator: Generated maze.

    Returns:
        Shortest path as a list of coordinates.

    Raises:
        ValueError: If no path exists between entry and exit.
    """

    solver = MazeSolver(
        start=generator.entry,
        end=generator.exit_maze
    )

    solution = solver.solve(generator)

    if solution is None:
        raise ValueError("No valid path exits between entry and exit")
    return solution


def export_maze(
        generator: Generator,
        solution: list[tuple[int, int]],
        output_file: str
) -> None:
    """
    Export the generated maze to the output file.

    Args:
        generator: Generated maze.
        solution: Shortest path from entry to exit, as a list of
            (x, y) coordinates.
        output_file: Output filename.
    """
    exporter = MazeExporter(generator.grid)
    exporter.export(
        output_file,
        entry=generator.entry,
        exit_maze=generator.exit_maze,
        solution=solution,
    )


def check_terminal(width: int, height: int) -> bool:
    """
    Check whether a maze of the given size fits in the terminal.

    Each cell prints as 4 characters wide (1 junction + 3-char wall),
    plus 1 final junction, so a maze row is (width * 4 + 1) columns.
    Each row prints an h_line, and every row but the last also
    prints a v_line, so the maze is (height * 2 + 1) lines tall.

    Args:
        width: Maze width in cells.
        height: Maze height in cells.

    Returns:
        True if the current terminal window is large enough.
    """
    need_cols = width * 4 + 1
    need_lines = height * 2 + 1
    tram_size = shutil.get_terminal_size()

    return (
        tram_size.columns >= need_cols
        and tram_size.lines >= need_lines
    )


def run_interactive(
        generator: Generator,
        solution: list[tuple[int, int]],
        config: dict[str, Any]
) -> None:
    """
    Display the maze and handle user interaction.

    Args:
        generator: Generated maze.
        solution: Shortest path.
        config: Parsed configuration, needed to rebuild the maze
            from scratch on "Re-generate" (a fresh Generator is
            required — reusing the same instance would duplicate
            its grid rows, since create_grid() appends rather than
            resets).
    """

    if not check_terminal(generator.width, generator.height):
        need_cols = generator.width * 4 + 1
        need_lines = generator.height * 2 + 1
        print(
            "Terminal window is too small to display this maze.\n"
            f"Required: at least {need_cols} columns x "
            f"{need_lines} lines.\n"
            "Please enlarge your terminal window and rerun the program."
        )
        return
    state: dict[str, bool] = {"resized": False}
    install_resize_watcher(state)

    wait_for_terminal_fit(generator.width, generator.height)
    renderer = RendererMaze(
        generator=generator,
        solution=solution,
        show_solution=False
    )

    while True:
        if not check_terminal(generator.width, generator.height):
            need_cols = generator.width * 4 + 1
            need_lines = generator.height * 2 + 1

            print(
                "\033[2J\033[H"
                "Terminal window is too small to display this maze.\n"
                f"Required: at least {need_cols} columns x "
                f"{need_lines} lines.\n"
                "Please enlarge your terminal window."
            )

            try:
                input("Press Enter after enlarging the terminal...")
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                return

            continue
        render_with_resize_guard(renderer, state)
        renderer.print_menu()

        try:
            choice = input().strip()
        except InterruptedError:
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        if choice == "1":
            new_gene = bulid_generator(config)
            new_solu = solve_maze(new_gene)
            renderer.generator = new_gene
            renderer.solution = new_solu

        elif choice == "2":
            renderer.toggle_solution()
        elif choice == "3":
            renderer.change_theme()
        elif choice == "4":
            print("Bye!")
            return
        else:
            print("Invalid choice. Plase choose 1, 2, 3, 4.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python3 a_maze_ing.py config.txt",
            file=sys.stderr
        )
        sys.exit(1)

    config_path = sys.argv[1]
    try:
        config = load_config(config_path)
        generator = bulid_generator(config)
        solution = solve_maze(generator)
        output_file = config["OUTPUT_FILE"]
        if not isinstance(output_file, str):
            raise TypeError("OUTPUT_FILE must be a string.")
        export_maze(generator, solution, output_file)
        run_interactive(generator, solution, config)
    except (FileNotFoundError, ValueError, TypeError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
