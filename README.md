*This activity has been created as part of the 42 curriculum by sabu-kha, aalshoub.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generation project from the 42 curriculum. The goal is to build a
grid-based maze from a configuration file, guarantee a visible "42" pattern inside it,
compute a valid shortest path between an entry and an exit, and encode the whole
structure into a compact hexadecimal file format.

The program reads a configuration file describing the maze size, entry/exit
coordinates, and generation mode, builds the maze according to that mode, solves it,
writes the result to an output file, and renders it in the terminal with a small
interactive menu.

The project enforces a concrete understanding of maze-generation theory by requiring
two distinct generation modes — a perfect maze (a spanning tree with no loops) and a
playable, loop-containing board — both built from the same underlying carving
algorithm, plus a shortest-path solver and a reusable, standalone generation package.

## Instructions

### Installation

```bash
make install
```

Installs the development dependencies (`mypy`, `flake8`) via `pip`. The maze engine
itself has no third-party runtime dependencies — it only uses the Python standard
library (`random`, `collections.deque`, `enum`, `os`, `typing`).

Requires **Python 3.10+**.

### Usage

```bash
python3 a_maze_ing.py config.txt
```

- `a_maze_ing.py` is the mandatory entry-point filename.
- `config.txt` is the only argument — any file following the same `KEY=VALUE` format
  works.

### Makefile

| Target | Effect |
|---|---|
| `make install` | Install dependencies. |
| `make run` | Run the program. |
| `make debug` | Run under Python's built-in debugger (`pdb`). |
| `make lint` | `flake8` + `mypy` with the mandatory flag set. |
| `make lint-strict` | `flake8` + `mypy --strict`. |
| `make clean` | Remove `__pycache__`, `.mypy_cache`, and `.pyc` files. |

### Configuration file

One `KEY=VALUE` pair per line. Blank lines and lines starting with `#` are ignored.

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width, in cells | `WIDTH=20` |
| `HEIGHT` | Maze height, in cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `x,y` | `ENTRY=0,0` |
| `EXIT` | Exit coordinates `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` for a perfect maze, `False` for a playable board | `PERFECT=True` |

`parser.py` validates every field: `WIDTH`/`HEIGHT` must be integers, `ENTRY`/`EXIT`
must be `int,int` pairs, `PERFECT` must be exactly `True` or `False`, `OUTPUT_FILE`
cannot be empty, and any unrecognized key raises a clear error instead of failing
silently or crashing.

### Output file format

The maze is written using one hexadecimal digit per cell. Each digit's four bits
encode which walls are closed:

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

`1` = wall closed, `0` = wall open. Cells are written row by row, one row per line.
After a blank line, three more lines follow: the entry coordinates, the exit
coordinates, and the shortest path from entry to exit expressed with `N`/`E`/`S`/`W`
letters. Every line ends with `\n`.

```
95153915395517951511511 53
EBABAE812853C1412BA81281 2
...

1,1
19,14
SWSESWSESWSSSEESEEENEESE...
```

### Usage examples

```bash
# Generate and display a maze from the default config
python3 a_maze_ing.py config.txt

# Generate a perfect maze into a custom output file
echo "WIDTH=25
HEIGHT=20
ENTRY=0,0
EXIT=24,19
OUTPUT_FILE=perfect_maze.txt
PERFECT=True" > perfect_config.txt
python3 a_maze_ing.py perfect_config.txt

# Generate a playable (looped) board
echo "WIDTH=25
HEIGHT=20
ENTRY=0,0
EXIT=24,19
OUTPUT_FILE=playable_maze.txt
PERFECT=False" > playable_config.txt
python3 a_maze_ing.py playable_config.txt
```

Error cases — the program prints a clear message and exits without crashing:

- Configuration file not found.
- Malformed lines (`KEY` without `=VALUE`, unknown keys).
- `WIDTH`/`HEIGHT` not integers, or `ENTRY`/`EXIT` not in `x,y` format.
- Entry/exit coordinates outside the maze bounds, or not on the maze's edge.
- Maze too small to fit the "42" pattern (a warning is printed and the pattern is
  skipped, generation still succeeds).

## Algorithms

### Overview: two generation modes, one carving pass

Every maze starts from the same base structure: an empty grid where every cell has all
four walls closed, built by `Generator.create_grid()`. From there, one carving pass
(iterative depth-first search) always runs first. What differs between the two modes is
what happens *after* that pass:

| Mode | Function | What runs |
|---|---|---|
| Perfect | `perfect()` | DFS carving only |
| Playable | `none_perfect()` | DFS carving, then loop addition (`add_loop`) |

Both modes reserve the "42" pattern cells before carving begins, and both are solved
afterward with the same BFS shortest-path search.

### 1. Maze carving — Iterative DFS / Recursive Backtracking

File: `mazegen/generator.py` (`Generator.run_backtracking`)

Starting from the entry cell, the algorithm carves a passage into a random unvisited
neighbor, moves into it, and repeats. When it reaches a cell with no unvisited
neighbors, it backtracks to the previous cell with unexplored options and continues
from there, until every reachable cell has been visited exactly once. It is implemented
iteratively with an explicit stack rather than recursively, to avoid Python's recursion
depth limit on large mazes.

```
push entry cell, mark visited
while stack is not empty:
    peek at top of stack
    if it has an unvisited, in-bounds, non-reserved neighbor:
        pick one at random
        open the wall between them on both cells
        mark it visited, push it
    else:
        pop the stack   # backtrack
```

**Complexity argument:**

- Each cell is visited exactly once, and each visit does O(1) work to pick and open a
  wall to a neighbor → **O(W×H)** total, linear in the number of cells.
- Because every cell is reached through exactly one connection, the result is
  mathematically a **spanning tree** of the grid.

**Why this algorithm:** a spanning tree is, by definition, a structure with exactly one
path between any two nodes — so the "exactly one path between entry and exit" perfect
maze requirement is satisfied automatically, with no extra validation step needed.
Recursive backtracking also produces long, winding corridors instead of short,
choppy branches, which reads visually as a proper maze rather than a random grid with
holes in it.

**Wall consistency:** `remove_wall_between` always opens the wall on *both* cells that
share it (e.g., the current cell's `east` and the neighbor's `west`), which is what
guarantees the output stays coherent — no cell can end up with a wall its neighbor
doesn't agree on.

**The "42" pattern:** before carving starts, `reserve_42_cells()` computes the
coordinates of a fixed 8×5 pattern spelling "42", centered on the grid (only if
`height >= 7` or `width >= 10`; otherwise the pattern is skipped and a warning is
printed). These coordinates are excluded from every neighbor lookup during carving, so
they are never visited — and since every cell starts fully walled, their walls simply
stay closed, producing the pattern without any separate drawing pass.

### 2. Loop addition for playable boards — O(W×H) random wall removal

File: `mazegen/generator.py` (`add_loop`)

A plain DFS carve always produces a tree — zero loops by construction — which fails the
"at least two independent routes" requirement for `PERFECT=False`. A second pass runs
afterward to reintroduce a controlled number of loops:

```
attempts = (width * height) // 10
repeat `attempts` times:
    pick a random non-reserved cell
    pick one of its still-closed neighbors
    if opening that wall would create a fully open 3x3 area: skip
    otherwise: open the wall
```

**Complexity argument:** the number of attempts scales linearly with the maze area
(`W×H / 10`), and each attempt does O(1) neighbor/area checks → **O(W×H)** total.

**Why this approach:** attempting a bounded, size-proportional number of extra
connections keeps the board loopy without over-opening it into a featureless open
field. The 3×3 open-area check (`can_open_wall` / `is_open_area`) is what directly
enforces the subject's "no corridor wider than 2 cells" rule — any wall removal that
would create a fully open 3×3 block is rejected before it happens.

### 3. Shortest-path solving — BFS

File: `mazegen/solver.py` (`MazeSolver.solve`)

The entry cell is pushed into a FIFO queue. On each step, the algorithm pops from the
front, and for every neighbor reachable through an open wall that hasn't been visited
yet, it records where that neighbor was reached from and pushes it onto the queue. The
moment the exit cell is popped, the search stops.

```
enqueue(start), visited = {start}
while queue is not empty:
    current = dequeue()
    if current == end: return reconstructed path
    for neighbor in open_neighbors(current):
        if neighbor not visited:
            mark visited, record parent, enqueue(neighbor)
return None   # no path exists
```

**Complexity argument:**

- Every cell is enqueued and dequeued at most once, and each dequeue examines at most 4
  neighbors → **O(W×H)** time and space in the worst case.
- Because cells are processed strictly in FIFO order, BFS explores the maze in
  expanding "rings" of increasing distance from the entry — so the first time the exit
  is reached is guaranteed to be via the shortest possible route.

**Why BFS and not DFS:** the maze is an unweighted graph — every move costs exactly one
step — and BFS is the algorithm that *guarantees* the shortest path in that setting,
whereas DFS would only guarantee finding *some* path, not necessarily the shortest one.

### Terminal rendering

File: `mazegen/renderer.py` (`RendererMaze`)

The maze is drawn using Unicode box-drawing characters, with 16 possible wall-junction
glyphs chosen per intersection based on which of the four surrounding walls are
present. The reserved "42" cells are rendered with distinct double-line glyphs
(`═ ║ ╬ …`) and a solid block fill, so the pattern is visually set apart from ordinary
corridors. The entry is shown as a green `●`, the exit as a red `■`, and the solution
path (when toggled on) as a colored `•` trail. Wall color cycles through four presets.
An interactive menu supports re-generating the maze, toggling the solution path,
changing the wall color, and quitting.

## Project Structure

```
A_maze_ing/
├── Makefile
├── LICENSE.md
├── README.md
├── a_maze_ing.py         # entry point
├── config.txt             # default configuration
├── parser.py              # config file parsing and validation
├── pyproject.toml
├── requirements.txt
├── mazegen/                # reusable, standalone package
│   ├── __init__.py
│   ├── cell.py             # Cell: position, visited flag, 4 walls
│   ├── generator.py        # Generator, perfect(), none_perfect(), add_loop
│   ├── solver.py            # MazeSolver — BFS shortest path
│   ├── exporter.py          # MazeExporter — grid to hexadecimal file
│   └── renderer.py           # RendererMaze — terminal display + menu
└── flowchart/                 # design diagrams (the plan)
```

## The `mazegen` reusable package

The generation and solving logic is self-contained in `mazegen/`, independent of the
config parser, renderer, and CLI, so it can be installed and used in another project on
its own:

```python
from mazegen import Generator, perfect, none_perfect
from mazegen.solver import MazeSolver
from mazegen.exporter import MazeExporter

generator = Generator(
    entry=(0, 0),
    exit_maze=(19, 14),
    width=20,
    height=15,
    seed=42,           # None for a different maze every run
)

grid = perfect(generator)          # exactly one path, no loops
# grid = none_perfect(generator)   # playable board with loops

# grid[y][x] is a Cell with .north / .east / .south / .west booleans (True = closed)

solver = MazeSolver(start=(0, 0), end=(19, 14))
path = solver.solve(generator)     # list[(x, y)] from entry to exit, or None

MazeExporter(grid).export("maze.txt")
```

The structure returned by `Generator`/`perfect`/`none_perfect` (a grid of `Cell`
objects) is not the same representation as the hexadecimal output file —
`MazeExporter` performs that conversion.

### Building the package

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade build
python3 -m build
# -> dist/mazegen-<version>-py3-none-any.whl
# -> dist/mazegen-<version>.tar.gz
```

```bash
pip install mazegen-<version>-py3-none-any.whl
```

## Testing

```bash
pytest test/
```

| File | Covers |
|---|---|
| `test_generator.py` | Grid creation, "42" reservation, entry/exit validation |
| `test_solver.py` | BFS fin  maze generation, mazegen package, solver> |ds a solution, starts at entry, ends at exit |
| `test_renderer.py` | Initial renderer state, cell content rendering |
| `test_cell.py` | Wall open/close behavior |

## Known Limitations

- `a_maze_ing.py` — the entry point — is not yet wired together; `parser.py`,
  `mazegen/`, and `mazegen/renderer.py` currently work independently but are not yet
  connected into a single CLI flow.
- `parser.py` defines its constructor as `_init_` instead of `__init__`, so
  `Parser()` currently does not initialize `self.filename` as intended.
- The sample `config.txt` uses `EXIST=19,14` instead of `EXIT=19,14`, and includes a
  `SEED` key not yet recognized by `parser.py`.
- `LICENSE.md` is currently empty; the subject requires an explicit license permitting
  reuse of the `mazegen` package by later projects.
- Only a terminal renderer is implemented; no graphical (MLX) display exists.

## Contributors

| Login | Contributions |
|---|---|
| `sabu-kha` |  maze_solver,maze_exporter,config parsing,licences, |
| `aalshoub` |  rendering, mazegenerator,makefile,main file,cell |

## Resources

- Maze generation algorithms — depth-first search / recursive backtracking, Prim's,
  and Kruskal's algorithms for maze generation.
- Introduction to graph theory — spanning trees, and why they guarantee exactly one
  path between any two nodes.
- Breadth-first search and shortest paths in unweighted graphs.
- Python documentation: `typing`, `collections.deque`, `enum`, `pytest`, `flake8`,
  `mypy`.

## AI Usage
- for explaining and understanding Algorithms better
