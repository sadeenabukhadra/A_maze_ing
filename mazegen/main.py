from mazegen.generator import Generator
from mazegen.renderer import MazeRenderer


def main():

    # Maze size
    width = 10
    height = 10

    # Create maze generator
    generator = Generator(
        width=width,
        height=height,
    )

    # Generate maze
    generator.generate()

    # Create renderer
    renderer = MazeRenderer(
        generator=generator,
        show_path=True,
    )

    # Optional colors
    renderer.set_wall_color("cyan")
    renderer.set_path_color("yellow")
    renderer.set_pattern_color("magenta")
    renderer.set_entry_color("green")
    renderer.set_exit_color("red")

    # Print maze
    renderer.print_maze()


if __name__ == "__main__":
    main()
