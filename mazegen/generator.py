from random import seed
from cell import Cell
from abc import ABC, abstractmethod
from collections.abc import Callable


class MazeGenenrator(ABC):
    def __init__(
            self, WIDTH: int, HEIGHT: int,
            ENTRY: tuple[int, int], Exit: tuple[int, int],
            SEED: int
            ) -> None:
        ...

    @abstractmethod
    def create_grid(self) -> None:
        ...

    @abstractmethod
    def genrator_maze(self) -> None:
        ...


class PerfctMaze(MazeGenenrator):
    def create_grid(self):
        return super().create_grid()

    def genrator_maze(self):
        return super().genrator_maze()


class NonePerfectMaze(MazeGenenrator):
    def create_grid(self):
        return super().create_grid()

    def genrator_maze(self):
        return super().genrator_maze()

    def add_loop():
        ...


def get_maze(maze: Callable):
    ...

if __name__ == "__main__":
    ...

