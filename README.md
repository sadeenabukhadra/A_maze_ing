*This activity has been created as part of the 42 curriculum by sabu-kha and aalshobaki.*

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
 - Python 3.14.6
 - Dependens listed in requirments.txt/
