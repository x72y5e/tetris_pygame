import sys
import pygame
from pygame import Surface
from pygame.locals import *
import numpy as np
from typing import List, Tuple, NewType
from shape import Shape

# TODO: shapes can overlap when moving


Coord = NewType("coord", Tuple[int, int])

class Grid(object):

    def __init__(self, dims: Tuple[int, int]):
        grid_dims = (*dims, 3)
        self.block_positions = np.zeros(grid_dims, dtype=np.uint8)

    def update(self, fallen_shape: Shape):
        if sum([1 for _, y in fallen_shape.blocks if y == 0]):
            print("GAME OVER.")
            #sys.exit(0)
        for x, y in fallen_shape.blocks:
            self.block_positions[x, y] = fallen_shape.colour

    def clear_line(self, rate: int) -> int:
        y = np.where(self.block_positions.all(axis=0))
        if self.block_positions[:, y].any():
            self.block_positions = np.roll(self.block_positions, 1, axis=1)
            self.block_positions[:, 0, :] = 0.
            return rate + 0.2
        return rate

    def draw_grid(self, surf: Surface) -> None:
        pygame.surfarray.blit_array(surf, self.block_positions)

    def game_over(self, surf: Surface, screen: Surface, dims: Tuple[int, int], clock: pygame.time.Clock) -> None:
        for _ in range(10):
            self.block_positions += 25
            pygame.surfarray.blit_array(surf, self.block_positions)
            surf2 = pygame.transform.scale(surf, dims)
            screen.blit(surf2, (0, 0))
            pygame.display.update()
            clock.tick(4)


def run(dims: Tuple[int, int] = (400, 400)):
    reduced_dims = (dims[0] // 10, dims[1] // 10)
    pygame.init()
    screen = pygame.display.set_mode(dims)
    display_surf = pygame.Surface(reduced_dims)
    clock = pygame.time.Clock()
    rate = 5
    done = False

    grid = Grid(reduced_dims)
    current_shape = Shape(reduced_dims)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == KEYDOWN and event.key == K_LEFT:
                current_shape.move("l", grid.block_positions)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                current_shape.move("r", grid.block_positions)
            elif event.type == KEYDOWN and event.key == K_UP:
                current_shape.rotate(grid.block_positions)
            elif event.type == KEYDOWN and event.key == K_DOWN:
                current_shape.drop(grid.block_positions)

        grid.draw_grid(display_surf)
        current_shape.draw_shape(display_surf)

        current_shape.step(grid.block_positions)

        if not current_shape.can_move:
            if current_shape.game_over:
                grid.game_over(display_surf, screen, dims, clock)
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == "K_SPACE":
                        print("restarting")
                        grid = Grid(reduced_dims)
                        current_shape = Shape(reduced_dims)
                    else:
                        sys.exit(0)

            grid.update(current_shape)
            current_shape = Shape(reduced_dims)
            rate = grid.clear_line(rate)

        surf = pygame.transform.scale(display_surf, dims)
        screen.blit(surf, (0, 0))
        pygame.display.update()

        clock.tick(int(rate))


if __name__ == '__main__':
    run()
