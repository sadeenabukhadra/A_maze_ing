"""
Maze package.

Provides the main classes and functions for maze generation,
solving, and manipulation.
"""

from .cell import Cell
from .generator import Generator, perfect, none_perfect
from .solver import MazeSolver

__all__ = [
    "Cell",
    "Generator",
    "MazeSolver",
    "perfect",
    "none_perfect",
]
