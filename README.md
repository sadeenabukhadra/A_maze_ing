* This activity has been created as part of the 42 curriculum by sabu-kha and aalshobaki.*

# A-Maze-ing

This is the way. 

# Description
A-Maze-ing is a python maze generator . Given a simple `config.txt` file ,
it builds a grid- based maze , guarantees a visible "42" pattern made of fully closed cells ,writes the result to hexadecimal output file , and displays it - either  in the terminal or through a graphical window - with interactive controls to regenerate the maze , toggle the solution path , and change the wall colors .

 The maze can be generated in two modes,controlled by the `PERFECT` flag:

- **`PERFECT=True`** — a perfect maze: exactly one path between the entry and the exit,
  no loops at all (the classic academic/lab maze).
- **`PERFECT=False`** (default) — a Pac-Man-style playable board: fully connected, open
  corners and center, at least two independent routes between any two points, and as
  few dead-ends as possible.

The maze generation logic is also packaged as a standalone, reusable, pip-installable
module (`mazegen`) so it can be dropped into a future project.


# Instructions

# Requirements 

- Python 3.10+
- Dependencies listed in requirements.txt / pyproject.toml

# Usage 
     python3 a_maze_ing.py config.txt

# Makefile
   
    make install       # install dependencies (pip)
    make run            # run a_maze_ing.py with the default config.txt
    make debug          # run the main script under pdb
    make lint           # flake8 + mypy checks
    make lint-strict     # flake8 + mypy --strict (optional, stricter)
    make clean          # remove __pycache__, .mypy_cache, build artifacts, etc.


 # Building the reusable package
The reusable maze-generation module is distributed as a standalone mazegen-* package (both .tar.gz and .whl can be produced) built from the mazegen/ directory using the 
 standard Python build tooling:
   
     python3 -m venv .venv
     source .venv/bin/activate
     pip install --upgrade build
     python3 -m build
     # -> dist/mazegen-<version>-py3-none-any.whl
     # -> dist/mazegen-<version>.tar.gz

# Configuration file format
config.txt contains one KEY=VALUE pair per line. Lines starting with # are comments and are ignored.

# Configuration file format

config.txt contains one KEY=VALUE pair per line. Lines starting with # are comments and are ignored.

| Key             | Description                        | Example                |
| --------------- | ---------------------------------- | ---------------------- |
| **WIDTH**       | Maze width (number of cells)       | `WIDTH=20`             |
| **HEIGHT**      | Maze height (number of cells)      | `HEIGHT=15`            |
| **ENTRY**       | Entry coordinates (x,y)            | `ENTRY=0,0`            |
| **EXIT**        | Exit coordinates (x,y)             | `EXIT=19,14`           |
| **OUTPUT_FILE** | Output filename                    | `OUTPUT_FILE=maze.txt` |
| **PERFECT**     | Whether the maze is a perfect maze | `PERFECT=False`        |


A default config.txt is provided at the root of this repository.

# Output file format

The maze is written using one hexadecimal digit per cell. Each digit encodes which of the 4 walls (North, East, South, West — bits 0 to 3, LSB first) are closed (1) or open (0). Cells are stored row by row, one row per line. After a blank line, three more lines follow: the entry coordinates, the exit coordinates, and the shortest path from entry to exit expressed with N/E/S/W letters. All lines end with \n.

# Maze generation algorithm

The maze is generated with a Depth-First Search / Recursive Backtracking algorithm: starting from the entry cell, the algorithm carves a passage into a random unvisited neighbor, recursing until it hits a dead end, then backtracking to the last cell with an unvisited neighbor, until every cell has been visited.

- Why this algorithm: it naturally produces a perfect maze (a spanning tree of the grid) with long, winding corridors and relatively few short dead-ends, it's simple to reason about and to implement recursively (or iteratively with a stack), and it's easy to extend afterward — when PERFECT=False, extra passages (loops) are carved back into the perfect maze produced by DFS to guarantee full connectivity, open corners and center, and at least two independent routes, while keeping dead-ends rare.
- The "42" pattern is stamped as a set of fully closed cells once the base structure exists, and an optional wall-consistency check can be run afterward.
- Solving (finding the shortest path between entry and exit) is done with a Breadth-First Search (BFS), which is guaranteed to find the shortest path in an unweighted graph such as this cell grid.

# Reusable module

The reusable part of the code lives in the mazegen/ package:

 - mazegen/generator.py — the MazeGenerator class: builds the grid, runs the DFS generation, adds loops / the "42" pattern depending on the requested mode.
- mazegen/cell.py — the Cell class representing a single grid cell and its walls.
- mazegen/solver.py — BFS shortest-path solver.
- mazegen/exporter.py — converts the maze structure to the hexadecimal output format.
- mazegen/renderer.py — terminal / graphical rendering of the maze.
 # Basic usage
   
    from mazegen import MazeGenerator

    # Instantiate a generator with custom parameters
    maze = MazeGenerator(width=20, height=15, seed=42, perfect=False)
    # Generate the maze
    maze.generate()

    # Access the generated structure (grid of Cell objects)
    grid = maze.grid

    # Access a solution (shortest path from entry to exit)
    path = maze.solve()

The structure exposed by MazeGenerator (a grid of Cell objects, each with its own north / east / south / west wall flags) is not the same representation as the hexadecimal output file — the export step in mazegen/exporter.py handles that conversion.

mazegen-*.whl / mazegen-*.tar.gz at the root of the repository bundle this module (code + this documentation) for pip installation in another project:


     pip install mazegen-1.0.0-py3-none-any.whl
# Visual representation
The maze can be displayed either as terminal ASCII art or through a graphical MLX-style window. Both display the walls, the entry (colored cell), the exit (colored cell), and the "42" pattern, and both support the same interactions:

1 - Re-generate a new maze and display it.
2 - Show/Hide the shortest valid path from entry to exit.
3 - Rotate/change the maze wall colors.
4 - Quit.
# Resources
- Maze generation algorithms — general overview of DFS/recursive-backtracking, Prim's, and Kruskal's algorithms for maze generation.
- Introduction to graph theory — background on spanning trees, used to understand why a perfect maze has exactly one path between any two cells.
- Python documentation: typing, argparse, unittest/pytest, flake8, mypy.

# AI usage

AI assistance was used during this project for:

- <describe here, e.g. "brainstorming edge cases for config-file validation">
- <describe here, e.g. "reviewing flake8/mypy warnings and suggesting fixes">
- <describe here, e.g. "drafting docstrings, later checked and adjusted manually">

All AI-generated suggestions were reviewed, tested, and understood by the team before being integrated, in line with the project's AI usage guidelines.

Team and project management
- Team members and roles:
   - <name> — <role, e.g. maze generation & mazegen package>
   - <name> — <role, e.g. rendering & user interaction>
   - <name> — <role, e.g. config parsing, testing, packaging>
- Planning: <describe initial planning and how it evolved — milestones, adjustments made along the way>
- What worked well / what could be improved: <retrospective notes>
- Tools used: <e.g. Git/GitHub, project board, CI, specific linters, pair programming sessions, etc.>
# Project structure

     .
     ├── LICENSE.md
     ├── Makefile
     ├── README.md
     ├── a_maze_ing.py
     ├── config.txt
     ├── mazegen/
     │   ├── __init__.py
     │   ├── cell.py
     │   ├── exporter.py
     │   ├── generator.py
     │   ├── renderer.py
     │   └── solver.py
     ├── mazegen-<version>-py3-none-any.whl   # built package (or .tar.gz)
     ├── parser.py
     ├── pyproject.toml
     ├── requirements.txt
     └── test/
        ├── __init__.py
        ├── test_cell.py
        ├── test_generator.py
        ├── test_renderer.py
        └── test_solver.py
