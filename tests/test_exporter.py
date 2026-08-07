from generator import Generator, perfect
from exporter import MazeExporter


def main() -> None:

    generator = Generator(entry=(0, 0), exit_maze=(4, 4), width=5, height=5, seed=42)

    grid = perfect(generator)

    exporter = MazeExporter(grid)

    exporter.export("test_maze.txt")

    print("Maze exported ")


main()
