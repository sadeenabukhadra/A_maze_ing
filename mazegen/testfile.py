try:
    from generator import Generator
except ImportError:
    from .generator import Generator

try:
    from solver import MazeSolver
except ImportError:
    from .solver import MazeSolver


class MazeRenderer:
    """
    Render the maze using Unicode box-drawing characters.
    """

    COLORS = {
        "reset": "\033[0m",
        "black": "\033[30m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }

    # Heavy Unicode Box Drawing
    BOX_CHARS = {
        0: " ",
        1: "━",
        2: "━",
        3: "━",
        4: "┃",
        5: "┏",
        6: "┓",
        7: "┳",
        8: "┃",
        9: "┗",
        10: "┛",
        11: "┻",
        12: "┃",
        13: "┣",
        14: "┫",
        15: "╋",
    }

    def __init__(
        self,
        generator: Generator,
        show_path: bool = False,
    ) -> None:

        self.generator = generator
        self.show_path = show_path

        self.wall_color = "cyan"
        self.path_color = "yellow"
        self.pattern_color = "magenta"
        self.entry_color = "green"
        self.exit_color = "red"

    #######################################################

    def set_wall_color(self, color: str):

        if color in self.COLORS:
            self.wall_color = color

    def set_path_color(self, color: str):

        if color in self.COLORS:
            self.path_color = color

    def set_pattern_color(self, color: str):

        if color in self.COLORS:
            self.pattern_color = color

    def set_entry_color(self, color: str):

        if color in self.COLORS:
            self.entry_color = color

    def set_exit_color(self, color: str):

        if color in self.COLORS:
            self.exit_color = color

    #######################################################

    def render(self):

        width = self.generator.width
        height = self.generator.height

        grid = self.generator.grid
        reserved = self.generator.reserved_cells

        term_h = height * 2 + 1
        term_w = width * 2 + 1

        walls = [[False] * term_w for _ in range(term_h)]

        #######################################################
        # Build wall mask
        #######################################################

        for y in range(height):
            for x in range(width):

                cell = grid[y][x]

                cy = y * 2 + 1
                cx = x * 2 + 1

                if cell.status_wall("north"):
                    walls[cy - 1][cx] = True

                if cell.status_wall("south"):
                    walls[cy + 1][cx] = True

                if cell.status_wall("west"):
                    walls[cy][cx - 1] = True

                if cell.status_wall("east"):
                    walls[cy][cx + 1] = True

        #######################################################
        # Add intersections
        #######################################################

        for y in range(height + 1):
            for x in range(width + 1):

                ty = y * 2
                tx = x * 2

                connected = False

                for dy, dx in [
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1),
                ]:

                    ny = ty + dy
                    nx = tx + dx

                    if 0 <= ny < term_h and 0 <= nx < term_w and walls[ny][nx]:
                        connected = True
                        break

                if connected:
                    walls[ty][tx] = True

        #######################################################
        # Empty canvas
        #######################################################

        canvas = [[" "] * term_w for _ in range(term_h)]

        #######################################################
        # Draw walls
        #######################################################

        wall_color = self.COLORS[self.wall_color]

        for r in range(term_h):
            for c in range(term_w):

                if not walls[r][c]:
                    continue

                up = r > 0 and walls[r - 1][c]
                down = r < term_h - 1 and walls[r + 1][c]
                left = c > 0 and walls[r][c - 1]
                right = c < term_w - 1 and walls[r][c + 1]

                mask = (up << 3) | (down << 2) | (left << 1) | right

                ch = self.BOX_CHARS.get(mask, "╋")

                canvas[r][c] = wall_color + ch + self.COLORS["reset"]

        #######################################################
        # Reserved cells
        #######################################################

        p_color = self.COLORS[self.pattern_color]

        for x, y in reserved:

            canvas[y * 2 + 1][x * 2 + 1] = p_color + "█" + self.COLORS["reset"]

        #######################################################
        # Solution Path
        #######################################################

        if self.show_path:

            solver = MazeSolver(
                start=self.generator.entry,
                end=self.generator.exit_maze,
            )

            path = solver.solve(self.generator)

            if path:

                color = self.COLORS[self.path_color]

                for x, y in path:

                    canvas[y * 2 + 1][x * 2 + 1] = color + "•" + self.COLORS["reset"]

        #######################################################
        # Entry
        #######################################################

        ex, ey = self.generator.entry

        canvas[ey * 2 + 1][ex * 2 + 1] = (
            self.COLORS[self.entry_color] + "S" + self.COLORS["reset"]
        )

        #######################################################
        # Exit
        #######################################################

        ex, ey = self.generator.exit_maze

        canvas[ey * 2 + 1][ex * 2 + 1] = (
            self.COLORS[self.exit_color] + "E" + self.COLORS["reset"]
        )

        return "\n".join("".join(row) for row in canvas)

    #######################################################

    def print_maze(self):

        print(self.render())
