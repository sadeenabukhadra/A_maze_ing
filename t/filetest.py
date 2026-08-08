"""
Main entry point: generates a maze, solves it, and renders it
interactively in the terminal using RendererMaze.
"""

from generator import Generator, perfect, none_perfect
from solver import MazeSolver
from renderer import RendererMaze


WIDTH = 14
HEIGHT = 15
ENTRY = (0, 0)
EXIT_MAZE = (WIDTH - 1, HEIGHT - 1)
PERFECT = False


def build_maze(
    seed: int | None = None,
) -> tuple[Generator, list[tuple[int, int]] | None]:
    """Generate a new maze and compute its solution path."""
    gen = Generator(
        entry=ENTRY,
        exit_maze=EXIT_MAZE,
        width=WIDTH,
        height=HEIGHT,
        seed=seed,
    )

    if PERFECT:
        perfect(gen)
    else:
        none_perfect(gen)

    solver = MazeSolver(ENTRY, EXIT_MAZE)
    solution = solver.solve(gen)

    return gen, solution

def main() -> None:
    """Run the interactive maze rendering loop."""
    gen, solution = build_maze()
    view = RendererMaze(gen, solution=solution, show_solution=False)

    while True:
        view.render()
        view.print_menu()

        try:
            choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if choice == "1":
            gen, solution = build_maze()
            view.generator = gen
            view.solution = solution

        elif choice == "2":
            view.toggle_solution()

        elif choice == "3":
            view.change_color()

        elif choice == "4":
            print("Bye!")
            break

        else:
            print("Invalid option, press Enter to continue...")
            input()


if __name__ == "__main__":
    main()
