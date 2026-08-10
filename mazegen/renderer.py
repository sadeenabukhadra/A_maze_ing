"""
Maze Renderer Module.

Renders a maze in the terminal using Unicode box-drawing characters,
with special double-line styling for the reserved '42' pattern cells.
"""

from .generator import Generator
from enum import Enum
import os


def rgb_fg(r: int, g: int, b: int) -> str:
    """Build an ANSI true-color foreground escape sequence."""
    return f"\033[38;2;{r};{g};{b}m"


class Color(Enum):
    """Enumeration of ANSI color codes used for terminal output."""
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    RED = "\033[31m"


class RendererMaze:
    """Render a maze (walls, entry/exit, solution, and 42 pattern)."""
    def __init__(
        self,
        generator: Generator,
        solution: list[tuple[int, int]] | None = None,
        show_solution: bool = False
    ) -> None:
        """
        Initialize the renderer with a maze generator and display options.

        Args:
            generator: The Generator instance holding the maze grid.
            solution: Optional list of coordinates forming the solved path.
            show_solution: Whether the solution path is drawn by default.
        """
        self.generator = generator
        self.solution = solution
        self.show_solution = show_solution

        self.themes: list[dict[str, str]] = [
            {
                "name": "Ocean",
                "wall": rgb_fg(66, 165, 245),
                "pattern": rgb_fg(255, 255, 255),
            },
            {
                "name": "Sunset",
                "wall": rgb_fg(255, 138, 101),
                "pattern": rgb_fg(255, 213, 79),
            },
            {
                "name": "Forest",
                "wall": rgb_fg(129, 199, 132),
                "pattern": rgb_fg(200, 230, 201),
            },
            {
                "name": "Neon",
                "wall": rgb_fg(186, 104, 200),
                "pattern": rgb_fg(225, 190, 231),
            },
        ]

        self.curr_theme_index: int = 0
        self.curr_theme: dict[str, str] = self.themes[self.curr_theme_index]

        self.entry_fg = rgb_fg(76, 217, 100)
        self.exit_fg = rgb_fg(255, 69, 58)
        self.path_fg = rgb_fg(255, 255, 255)
        self.H_WALL = "━━━"
        self.H_EMPTY = "   "
        self.V_WALL = "┃"
        self.V_EMPTY = " "

        self.JUNCTIONS: dict[tuple[bool, bool, bool, bool], str] = {
            (True,  True,  True,  True): "╋",
            (True,  True,  True,  False): "┣",
            (True,  True,  False, True): "┫",
            (False, True,  True,  True): "┳",
            (True,  False, True,  True): "┻",

            (False, True,  True,  False): "┏",
            (False, True,  False, True): "┓",
            (True,  False, True,  False): "┗",
            (True,  False, False, True): "┛",

            (False, False, True,  True): "━",
            (True,  True,  False, False): "┃",
            (False, True,  False, False): "┃",
            (True,  False, False, False): "┃",
            (False, False, True,  False): "━",
            (False, False, False, True): "━",

            (False, False, False, False): " ",
        }

        self.RESERVED_H_WALL = "═══"
        self.RESERVED_V_WALL = "║"
        self.RESERVED_JUNCTIONS: dict[tuple[bool, bool, bool, bool], str] = {
            (True, True, True, True): "╬",
            (True, True, True, False): "╠",
            (True, True, False, True): "╣",
            (False, True, True, True): "╦",
            (True, False, True, True): "╩",
            (False, True, True, False): "╔",
            (False, True, False, True): "╗",
            (True, False, True, False): "╚",
            (True, False, False, True): "╝",
            (False, False, True, True): "═",
            (True, True, False, False): "║",
            (False, True, False, False): "║",
            (True, False, False, False): "║",
            (False, False, True, False): "═",
            (False, False, False, True): "═",
            (False, False, False, False): " ",
        }
        self.RESERVED_FILL_CHAR = "█"
        self.RESERVED_BLOCK = "███"

    def clear_screen(self) -> None:
        """Clear the terminal screen (cross-platform)."""
        if os.name == "net":
            os.system("cls")
        else:
            os.system("clear")

    def is_reseved(self, x: int, y: int) -> bool:
        """
        Check whether cell (x, y) belongs to the reserved '42' pattern.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.

        Returns:
            True if the cell is within bounds and reserved, else False.
        """
        w = self.generator.width
        h = self.generator.height

        if not (0 <= x < w and 0 <= y < h):
            return False
        return (x, y) in self.generator.reserved_cells

    def has_vwall(self, r: int, c: int) -> bool:
        """
        Check if a vertical wall segment exists between columns c-1 and c.

        Also hides the wall when both neighboring cells are reserved,
        so the '42' pattern renders as a merged block.

        Args:
            r: Row index.
            c: Column index of the wall segment.

        Returns:
            True if the wall segment should be drawn, else False.
        """

        grid = self.generator.grid
        w = self.generator.width
        h = self.generator.height

        if r < 0 or r >= h:
            return False
        if c == 0:
            return grid[r][0].west
        if c == w:
            return grid[r][w - 1].east

        left_rese = self.is_reseved(c - 1, r)
        right_rese = self.is_reseved(c, r)
        if left_rese and right_rese:
            return False
        return grid[r][c - 1].east or grid[r][c].west

    def has_hwall(self, r: int, c: int) -> bool:
        """
        Check if a horizontal wall segment exists between rows r-1 and r.

        Also hides the wall when both neighboring cells are reserved,
        so the '42' pattern renders as a merged block.

        Args:
            r: Row index of the wall segment.
            c: Column index.

        Returns:
            True if the wall segment should be drawn, else False.
        """

        grid = self.generator.grid
        w = self.generator.width
        h = self.generator.height

        if c < 0 or c >= w:
            return False
        if r == 0:
            return grid[0][c].north
        if r == h:
            return grid[h - 1][c].south

        top_rese = self.is_reseved(c, r - 1)
        bottom_rese = self.is_reseved(c, r)

        if top_rese and bottom_rese:
            return False

        return grid[r - 1][c].south or grid[r][c].north

    def both_reserved_h(self, r: int, c: int) -> bool:
        """True if the two cells sharing the horizontal segment at (r, c)
        are both reserved '42' cells."""
        return self.is_reseved(c, r - 1) and self.is_reseved(c, r)

    def both_reserved_v(self, r: int, c: int) -> bool:
        """True if the two cells sharing the vertical segment at (r, c)
        are both reserved '42' cells."""
        return self.is_reseved(c - 1, r) and self.is_reseved(c, r)

    def v_boundray(self, r: int, c: int) -> bool:
        """
        Check if the vertical wall at (r, c) sits on the 42 pattern edge.

        True only when exactly one of the two neighboring cells
        (c-1, r) and (c, r) is reserved (i.e. a boundary, not interior).

        Args:
            r: Row index.
            c: Column index of the wall segment.

        Returns:
            True if this segment is a boundary of the reserved pattern.
        """

        h = self.generator.height
        w = self.generator.width

        if r < 0 or r >= h:
            return False
        if c <= 0 or c >= w:
            return False

        left = self.is_reseved(c - 1, r)
        right = self.is_reseved(c, r)

        return left != right

    def h_boundray(self, r: int, c: int) -> bool:
        """
        Check if the horizontal wall at (r, c) sits on the 42 pattern edge.

        True only when exactly one of the two neighboring cells
        (c, r-1) and (c, r) is reserved (i.e. a boundary, not interior).

        Args:
            r: Row index of the wall segment.
            c: Column index.

        Returns:
            True if this segment is a boundary of the reserved pattern.
        """

        h = self.generator.height
        w = self.generator.width

        if c < 0 or c >= w:
            return False
        if r < 0 or r >= h:
            return False

        top = self.is_reseved(c, r - 1)
        bottom = self.is_reseved(c, r)

        return top != bottom

    def get_directions(
            self,
            r: int,
            c: int
    ) -> tuple[bool, bool, bool, bool]:
        """
        Collect the four wall states surrounding junction (r, c).

        Args:
            r: Row index of the junction.
            c: Column index of the junction.

        Returns:
            A (north, south, east, west) tuple of wall presence flags.
        """

        north = self.has_vwall(r - 1, c)
        south = self.has_vwall(r, c)
        west = self.has_hwall(r, c - 1)
        east = self.has_hwall(r, c)

        return north, south, east, west

    def junction_rese(
            self,
            r: int,
            c: int
    ) -> bool:
        """
        Check if junction (r, c) touches a boundary of the 42 pattern.

        Args:
            r: Row index of the junction.
            c: Column index of the junction.

        Returns:
            True if any adjacent wall segment is a reserved-pattern
            boundary, meaning the junction should use double-line style.
        """
        return (
            self.v_boundray(r - 1, c)
            or self.v_boundray(r, c)
            or self.h_boundray(r, c - 1)
            or self.h_boundray(r, c)
        )

    def get_junction(self, r: int, c: int) -> str:
        """
        Calculate the Unicode character to draw at junction (r, c).

        Args:
            r: Row index of the junction.
            c: Column index of the junction.

        Returns:
            The junction character: blank, a normal single-line glyph,
            or a double-line glyph when on the 42 pattern boundary.
        """

        directions = self.get_directions(r, c)
        if not any(directions):
            if self.junction_interior(r, c):
                return self.RESERVED_FILL_CHAR
            return " "
        if self.junction_rese(r, c):
            return self.RESERVED_JUNCTIONS.get(directions, "╬")
        return self.JUNCTIONS.get(directions, "╋")

    def junction_interior(self, r: int, c: int) -> bool:
        corners = [
            (c - 1, r - 1),
            (c, r - 1),
            (c - 1, r),
            (c, r),
        ]

        w = self.generator.width
        h = self.generator.height

        existing = [
            (x, y)
            for x, y in corners
            if 0 <= x < w and 0 <= y < h
        ]

        if not existing:
            return False

        return all(self.is_reseved(x, y) for x, y in existing)

    def get_content(self, x: int, y: int) -> str:
        """
        Return the formatted content to display inside cell (x, y).

        Priority order: entry marker, exit marker, solution path dot,
        reserved '42' block, then an empty cell.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.

        Returns:
            A color-coded string ready to be printed for this cell.
        """

        pos = (x, y)
        reset = Color.RESET.value

        if pos == self.generator.entry:
            return f"{self.entry_fg} ● {reset}"

        if pos == self.generator.exit_maze:
            return f"{self.exit_fg} ■ {reset}"

        if (
            self.show_solution and
            self.solution
            and pos in self.solution
        ):
            return f"{self.path_fg} • {reset}"

        if self.is_reseved(x, y):
            return f"{self.curr_theme['pattern']}{self.RESERVED_BLOCK}{reset}"
        return self.H_EMPTY

    def h_segment(
            self,
            r: int,
            c: int,
            wall_color: str,
            pattern_color: str
    ) -> str:
        """
        Pick the color for a horizontal wall segment at (r, c).

        Args:
            r: Row index of the wall segment.
            c: Column index.
            wall_color: ANSI color used for regular maze walls.
            pattern_color: ANSI color used for the 42 pattern walls.

        Returns:
            pattern_color if the segment touches a reserved cell,
            otherwise wall_color.
        """

        if (
            self.is_reseved(c, r - 1)
            or self.is_reseved(c, r)
        ):
            return pattern_color
        return wall_color

    def build_header(self) -> str:
        """Build a decorative header line showing the maze title and theme."""
        w = self.generator.width
        total_width = w * 4 + 1

        theme_name = self.curr_theme["name"]
        title = f" A-Maze-ing · {w}x{self.generator.height} · {theme_name} "

        wall_color = self.curr_theme["wall"]
        reset = Color.RESET.value

        inner_width = max(total_width - 2, len(title))
        line = title.center(inner_width, "─")

        return f"{wall_color}╭{line}╮{reset}"

    def build_footer(self) -> str:
        """Build a decorative footer line matching the header width."""
        w = self.generator.width
        total_width = w * 4 + 1

        wall_color = self.curr_theme["wall"]
        reset = Color.RESET.value

        return f"{wall_color}╰{'─' * (total_width - 2)}╯{reset}"

    def render(self) -> None:
        """Render the maze with dynamic walls,
        junctions, and reserved 42 blocks."""

        self.clear_screen()
        w = self.generator.width
        h = self.generator.height

        wall_color = self.curr_theme["wall"]
        pattern_color = self.curr_theme["pattern"]
        reset = Color.RESET.value
        print(self.build_header())

        for r in range(h + 1):

            h_line = ""
            for c in range(w):
                j_char = self.get_junction(r, c)
                has_wall = self.has_hwall(r, c)

                is_reseved_boun = self.h_boundray(r, c)

                if is_reseved_boun:
                    h_wall = (
                        self.RESERVED_H_WALL
                        if has_wall
                        else self.H_EMPTY
                    )
                    segment_color = pattern_color
                elif self.both_reserved_h(r, c):
                    h_wall = self.RESERVED_BLOCK
                    segment_color = pattern_color
                else:
                    h_wall = (
                        self.H_WALL
                        if has_wall
                        else self.H_EMPTY
                    )
                    segment_color = wall_color

                h_line += segment_color
                h_line += j_char
                h_line += h_wall

            j_end = self.get_junction(r, w)
            h_line += wall_color
            h_line += j_end
            h_line += reset

            print(h_line)

            if r < h:
                v_line = ""
                for c in range(w):
                    has_wall = self.has_vwall(r, c)

                    is_reseved_boun = self.v_boundray(r, c)

                    if is_reseved_boun:
                        v_char = (
                            self.RESERVED_V_WALL
                            if has_wall
                            else " "
                        )
                        segment_color = pattern_color
                    elif self.both_reserved_v(r, c):
                        v_char = self.RESERVED_BLOCK[0]
                        segment_color = pattern_color
                    else:
                        v_char = (
                            self.V_WALL
                            if has_wall
                            else self.V_EMPTY
                        )
                        segment_color = wall_color
                    content = self.get_content(c, r)

                    v_line += segment_color
                    v_line += v_char
                    v_line += reset
                    v_line += content

                v_end = (
                    self.V_WALL
                    if self.has_vwall(r, w)
                    else self.V_EMPTY
                )

                v_line += wall_color
                v_line += v_end
                v_line += reset
                print(v_line)
        print(self.build_footer())

    def print_menu(self) -> None:
        """Print the interactive option menu below the rendered maze."""
        reset = Color.RESET.value
        cyan = Color.CYAN.value

        print(f"\n{cyan}Options: {reset}")
        print("1: Re-generate new maze")
        print(
            f"2: Toggle solution path "
            f"(Currently: {self.show_solution})"
        )
        print("3: Change wall color")
        print("4: Quit")
        print("Choose an option: ", end="", flush=True)

    def change_theme(self) -> None:
        """Cycle to the next color theme in self.themes."""
        self.curr_theme_index = (
            (self.curr_theme_index + 1) % len(self.themes)
        )
        self.curr_theme = self.themes[self.curr_theme_index]

    def toggle_solution(self) -> None:
        """Toggle whether the solution path is displayed."""
        self.show_solution = not self.show_solution
