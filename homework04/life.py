""" "Game of life" creating """

import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """Initializing parameters"""

    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """Grid creating"""
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        if randomize:
            for i in range(self.cols):
                for j in range(self.rows):
                    grid[i][j] = random.randint(0, 1)

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """Finding the neighbours"""
        x, y = cell
        neib_cells = []
        for i in range(max(0, x - 1), min(self.rows, x + 2)):
            for j in range(max(0, y - 1), min(self.cols, y + 2)):
                if i == x and j == y:
                    continue
                neib_cells.append(self.curr_generation[i][j])
        return neib_cells

    def get_next_generation(self) -> Grid:
        """Next generation is"""
        out = [[0] * self.cols for _ in range(self.rows)]
        for x in range(self.rows):
            for y in range(self.cols):
                cells_neighbours = self.get_neighbours((x, y))
                alife_neibs = sum(cells_neighbours)

                if self.curr_generation == 0 and alife_neibs == 3:
                    out[x][y] = 1
                elif self.curr_generation == 1:
                    if alife_neibs >= 2 and alife_neibs <= 3:
                        out[x][y] = 1
        return out

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """

        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.max_generations is not None and self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, encoding="utf-8") as f:
            grid = [[int(cell) for cell in line.strip()] for line in f if line.strip()]
        game = GameOfLife((len(grid), len(grid[0])), randomize=False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            for line in self.curr_generation:
                f.write("".join(map(str, line)) + "\n")
