import sys
import numpy as np
import pygame
from pygame import Surface
from typing import Tuple


class Shape(object):

    def __init__(self, dims: Tuple[int, int], i: int = 0):
        origin = np.random.choice(range(2, dims[0] - 2))
        self.colour = np.random.randint(50, 256, size=3)
        if not i:
            i = np.random.randint(3)
        if i == 0:
            self.name = "square"
            self.blocks = [(origin, 0), (origin, 1), (origin + 1, 0), (origin + 1, 1)]
        elif i == 1:
            self.name = "offset"
            self.blocks = [(origin, 0), (origin, 1), (origin + 1, 1), (origin + 1, 2)]
        if i == 2:
            self.name = "bar"
            self.blocks = [(origin, 0), (origin, 1), (origin, 2), (origin, 3)]
        self.dims = dims
        self.can_move = True
        self.game_over = False

    def move(self, direction: str, grid: np.ndarray) -> None:
        if not self.can_move:
            return
        if direction == "l":
            new_coords = [(x - 1, y) for (x, y) in self.blocks]
            if not list(filter(lambda coord: coord[0] < 0, new_coords))\
                    and not np.any([grid[x, y] for (x, y) in new_coords]):
                self.blocks = new_coords
        elif direction == "r":
            new_coords = [(x + 1, y) for (x, y) in self.blocks]
            if not list(filter(lambda coord: coord[0] > self.dims[0] - 1, new_coords)) \
                    and not np.any([grid[x, y] for (x, y) in new_coords]):
                self.blocks = new_coords

    def rotate(self, grid: np.ndarray) -> None:
        if not self.can_move:
            return
        if self.name == "offset":
            (a, b), (i, j), (p, q), (v, w) = sorted(self.blocks)
            if i == p:
                # horizontal to vertical
                new_coords = [(a, b - 2), (i - 1, j), (p, q - 1), (v - 1, w + 1)]
            else:
                # vertical to horizontal
                new_coords = [(a + 2, b + 1), (i + 1, j), (p, q + 1), (v - 1, w)]
                # check if new positions are valid
            if not list(filter(lambda coord: coord[0] < 0 or coord[0] > self.dims[0] - 1, new_coords)) \
               and not np.any([grid[x, y] for (x, y) in new_coords]):
                   self.blocks = new_coords
        elif self.name == "bar":
            (a, b), (i, j), (p, q), (v, w) = sorted(self.blocks, key=lambda x: x[0])
            if a == i:
                # vertical to horizontal
                new_coords = [(a + 2, b + 1), (i + 1, j), (p, q - 1), (v - 1, w - 2)]
            else:
                # horizontal to vertical
                new_coords = [(a + 1, b - 1), (i, j), (p - 1, q + 1), (v - 2, w + 2)]
            if not list(filter(lambda coord: coord[0] < 0 or coord[0] > self.dims[0] - 1
                               or coord[1] > self.dims[1] - 1, new_coords)) \
               and not np.any([grid[x, y] for (x, y) in new_coords]):
                   self.blocks = new_coords

    def drop(self, grid: np.ndarray) -> None:
        new_coords = [(x, y + 5) for (x, y) in self.blocks]
        if not list(filter(lambda coord: coord[1] > self.dims[1] - 1, new_coords)) \
                and not np.any([grid[x, y] for (x, y) in new_coords]):
            self.blocks = new_coords

    def check_and_set_can_move(self, grid: np.ndarray) -> None:
        for (x, y) in self.blocks:
            if y >= grid.shape[1] - 1 or np.any(grid[x, y + 1] > 0):
                self.can_move = False
                if y <= 1:
                    self.game_over = True
                break

    def step(self, grid: np.ndarray):
        if self.can_move:
            self.blocks = [(x, min(self.dims[1] - 1, y + 1)) for (x, y) in self.blocks]
            self.check_and_set_can_move(grid)
        if self.game_over:
            print("GAME OVER")

    def draw_shape(self, surf: Surface):
        for (x, y) in self.blocks:
            block = pygame.Rect(x, y, 1, 1)
            pygame.draw.rect(surf, self.colour, block)
