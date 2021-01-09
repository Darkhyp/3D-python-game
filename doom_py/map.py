import numpy as np
import pygame
from numpy.core._multiarray_umath import ndarray

from .CONFIGS import *

# map0 = np.zeros((N_ROWS, N_COLS), dtype=np.int8)

# map0[0, :] = WALL
# map0[-1, :] = WALL
# map0[:, 0] = WALL
# map0[:, -1] = WALL
# map0[2, [2, 3]] = WALL
#
# map0[9, [5, 6]] = WALL
# map0[[7, 8, 9], 4] = WALL
from .tools import gradientRect

map0 = np.array(
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
     [1, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
     [1, 0, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 1],
     [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], dtype=np.int8).transpose()

grid_x = np.arange(N_COLS) * MAP_TILE_X
grid_y = np.arange(N_ROWS) * MAP_TILE_Y


class Map:
    def __init__(self, surface, map=map0):
        self.surface = surface
        self.map = map

        self.map_in_set = set()
        for ix in np.arange(self.map.shape[0]):
            for iy in np.arange(self.map.shape[1]):
                if self.map[ix,iy] == 1:
                    self.map_in_set.add((ix, iy))

    def draw(self):
        self.surface.fill(BLACK)
        for ix, x in enumerate(grid_x):
            for iy, y in enumerate(grid_y):
                if self.map[ix, iy]:
                    pygame.draw.rect(self.surface, DARKGREEN,
                                     (x, y, MAP_TILE_X, MAP_TILE_Y))

    def is_in_region(self, pos, region_number):
        ind_x, ind_y = np.where(self.map==region_number)
        N_map = ind_x.size

        if isinstance(pos[0], np.ndarray):
            N = pos[0].size
            is_in = np.logical_and(
                np.logical_and(ind_x.reshape(1, N_map) <= pos[0].reshape(N, 1) / TILE_X,
                               pos[0].reshape(N, 1) / TILE_X <= ind_x.reshape(1, N_map) + 1),
                np.logical_and(ind_y.reshape(1, N_map) <= pos[1].reshape(N, 1) / TILE_Y,
                               pos[1].reshape(N, 1) / TILE_Y <= ind_y.reshape(1, N_map) + 1)).any(axis=1)
        else:
            is_in = np.logical_and(
                np.logical_and(ind_x <= pos[0] / TILE_X,
                               pos[0] / TILE_X <= ind_x + 1),
                np.logical_and(ind_y <= pos[1] / TILE_Y,
                               pos[1] / TILE_Y <= ind_y + 1)).any()

        return is_in

    def is_in_region0(self, pos, region_number):
        ix = np.int8(pos[0] // TILE_X)
        iy = np.int8(pos[1] // TILE_Y)

        if isinstance(pos[0], np.ndarray):
            ix[ix < 0] = 0
            iy[iy < 0] = 0
            ix[ix >= N_COLS] = N_COLS - 1
            iy[iy >= N_ROWS] = N_ROWS - 1
        else:
            ix = ix if (ix >= 0) else 0
            iy = iy if (iy >= 0) else 0
            ix = ix if (ix < N_COLS) else N_ROWS - 1
            iy = iy if (iy < N_ROWS) else N_COLS - 1

        return self.map[ix, iy] == region_number

