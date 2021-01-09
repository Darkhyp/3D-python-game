"""
main class for "doom_py" classical game using pygame module
23/12/2020
Author A.V.Korovin [a.v.korovin73@gmail.com]
"""
import random
import sys
from math import cos, sin, degrees
import numpy as np

import pygame

from common import message_box, make_sound
from .CONFIGS import *
from .player import Player
from .map import Map
from .tools import gradientRect, mapping, to_index, check_intersection

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 32)


FOV_angle = np.linspace(-HALF_FOV, HALF_FOV, N_RAYS, endpoint=True).reshape(N_RAYS, 1)
cos_FOV_angle = np.cos(FOV_angle[:, 0])
sin_FOV_angle = np.sin(FOV_angle[:, 0])

# N_depth = MAX_DEPTH - PLAYER_RADIUS
# depth = np.arange(PLAYER_RADIUS,MAX_DEPTH).reshape(1, N_depth)
N_depth = MAX_DEPTH
depth = np.arange(MAX_DEPTH).reshape(1, N_depth)


class Game:
    """
    Main class for initializing the game engine and objects
    """
    score = []

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.map_surface = pygame.Surface((MAP_WIDTH*MAP_SCALE, MAP_HEIGHT*MAP_SCALE))
        pygame.display.set_caption('doom')

        self.game_over = True
        self.clock = pygame.time.Clock()

        self.map = Map(self.map_surface)
        self.player = Player(self.surface, self.map, (MAP_HALF_WIDTH, MAP_HALF_HEIGHT), 0, 2)

        self.texture = {'sky': pygame.image.load(SKY_IMAGE).convert(),
                        1: pygame.image.load(WALL_IMAGE).convert(),
                        2: pygame.image.load(FLOOR_IMAGE).convert()}


    def mainloop(self):
        # make_sound(2)
        # self.snake.start()

        # main loop
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    sys.exit()
            self.player.movement()

            self.background_draw()
            self.map.draw()
            self.ray_casting()
            self.draw_player_on_map()
            self.surface.blit(self.map_surface, MAP_POS)

            self.FPS_print()

            pygame.display.flip()
            self.clock.tick(FPS)

    def FPS_print(self):
        display_FPS = f'{self.clock.get_fps():>5.1f} FPS'
        text = myfont.render(display_FPS, True, (255, 255, 0))
        self.surface.blit(text,
                (self.surface.get_width()-text.get_width()-30, 30))

    def background_draw(self):
        # sky
        sky_offset = -5*degrees(self.player.angle) % DISPLAY_WIDTH
        self.surface.blit(self.texture['sky'], (sky_offset - DISPLAY_WIDTH, 0))
        self.surface.blit(self.texture['sky'], (sky_offset, 0))
        self.surface.blit(self.texture['sky'], (sky_offset + DISPLAY_WIDTH, 0))

        # gradientRect(self.surface, SKYBLUE, BLUE, pygame.Rect(0, 0, DISPLAY_WIDTH, HALF_HEIGHT))

        gradientRect(self.surface, DARKGREEN, BLACK, pygame.Rect(0, HALF_HEIGHT, DISPLAY_WIDTH, HALF_HEIGHT))

    def draw_player_on_map(self):
        pygame.draw.circle(self.map.surface, GREEN,
                           (self.player.pos[0]*MAP_SCALE, self.player.pos[1]*MAP_SCALE),
                           radius=PLAYER_RADIUS*MAP_SCALE)

    def ray_casting(self):
        return self.ray_casting2()
        # return self.ray_casting1()
        # return self.ray_casting0()

    def ray_casting2(self):
        # cos_a = np.cos(self.player.angle + FOV_angle[:, 0])
        # sin_a = np.sin(self.player.angle + FOV_angle[:, 0])
        cos_a, sin_a = cos(self.player.angle) * cos_FOV_angle - sin(self.player.angle) * sin_FOV_angle, \
                       sin(self.player.angle) * cos_FOV_angle + cos(self.player.angle) * sin_FOV_angle
        ox, oy = self.player.pos
        ix0, iy0 = mapping(self.player.pos)
        for i_a in range(N_RAYS):
            # verticals
            ix, dx = (ix0 + 1, 1) if cos_a[i_a] >= 0 else (ix0, -1)
            depth_v = MAX_DEPTH
            if cos_a[i_a] != 0:
                for nx in range(ix, N_COLS if dx > 0 else 0, dx):
                    x_v = nx*TILE_X
                    depth_v = (x_v - ox)/cos_a[i_a]
                    y_v = oy + depth_v * sin_a[i_a]
                    ny = int(y_v // TILE_Y)
                    if ny < 0 or ny >= N_ROWS:
                        break
                    # if (nx - 1 if dx < 0 else nx, int(y_v // TILE_Y)) in self.map.map_in_set:
                    n_texture_v = self.map.map[nx - 1 if dx < 0 else nx, ny]
                    if n_texture_v > 0:
                        break

            # horizontals
            iy, dy = (iy0 + 1, 1) if sin_a[i_a] >= 0 else (iy0, -1)
            depth_h = MAX_DEPTH
            if sin_a[i_a] != 0:
                for ny in range(iy, N_ROWS if dy > 0 else 0, dy):
                    y_h = ny*TILE_Y
                    depth_h = (y_h - oy)/sin_a[i_a]
                    x_h = ox + depth_h * cos_a[i_a]
                    nx = int(x_h//TILE_X)
                    if nx < 0 or nx >= N_COLS:
                        break
                    # if (int(x_h//TILE_X), ny-1 if dy<0 else ny) in self.map.map_in_set:
                    n_texture_h = self.map.map[nx, ny - 1 if dy < 0 else ny]
                    if n_texture_h > 0:
                        break

            # projection
            x, y, current_depth, offset, n_texture = (x_v, y_v, depth_v, int(y_v) % TILE, n_texture_v) if depth_v < depth_h else (x_h, y_h, depth_h, int(x_h) % TILE, n_texture_h)
            if current_depth > 0:
                pygame.draw.line(self.map.surface, GREEN if FOV_angle[i_a] == 0 else YELLOW,
                             (self.player.pos[0]*MAP_SCALE, self.player.pos[1]*MAP_SCALE),
                             (x*MAP_SCALE, y*MAP_SCALE))
            current_depth = max(current_depth, 0.002)

            current_depth *= cos(FOV_angle[i_a, 0])
            project_height = min(int(PROJ_COEFFICIENT/current_depth), 2*DISPLAY_HEIGHT)
            brightness = 255 / (1 + current_depth**2/2000)
            # i_color = (brightness, brightness//2, brightness//3)
            # pygame.draw.rect(self.surface, RED if FOV_angle[i_a] == 0 else i_color,
            #                  (i_a*SCALE, HALF_HEIGHT-project_height//2,
            #                   SCALE, project_height))
            wall_column = self.texture[n_texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (SCALE, project_height))
            wall_column.fill((brightness, brightness, brightness), None, pygame.BLEND_RGBA_MULT)
            self.surface.blit(wall_column, (i_a * SCALE, HALF_HEIGHT - project_height // 2))

    def ray_casting1(self):
        cos_a = np.cos(self.player.angle + FOV_angle[:, 0])
        sin_a = np.sin(self.player.angle + FOV_angle[:, 0])
        ix0, iy0 = to_index(self.plaayer.pos)
        ix, iy = to_index((self.player.pos[0] + MAX_DEPTH * cos_a, self.player.pos[1] + MAX_DEPTH * sin_a))
        for i_a in range(N_RAYS):
            # check verticals
            x_v, y_v, depth_v = check_intersection(self.player.pos[0], self.player.pos[1], ix0, ix[i_a], TILE_X, cos_a[i_a], sin_a[i_a],
                                                   lambda x, y: self.map.is_in_region((x, y), WALL))
            # check horizontals
            y_h, x_h, depth_h = check_intersection(self.player.pos[1], self.player.pos[0], iy0, iy[i_a], TILE_Y, sin_a[i_a], cos_a[i_a],
                                                   lambda y, x: self.map.is_in_region((x, y), WALL))

            x, y, depth = (x_v, y_v, depth_v) if depth_v < depth_h else (x_h, y_h, depth_h)
            if depth > 0:
                pygame.draw.line(self.map.surface, GREEN if FOV_angle[i_a] == 0 else YELLOW,
                             (self.player.pos[0]*MAP_SCALE, self.player.pos[1]*MAP_SCALE),
                             (x*MAP_SCALE, y*MAP_SCALE))

            current_depth = max(depth*cos(FOV_angle[i_a, 0]), 0.002)
            project_height = PROJ_COEFFICIENT/current_depth
            c = 255 / (1 + current_depth**2/2000)
            color = (c, c//2, c//3)
            pygame.draw.rect(self.surface, RED if FOV_angle[i_a]==0 else color,
                             (i_a*SCALE, HALF_HEIGHT-project_height//2,
                              SCALE, project_height))


    def ray_casting0(self):
        x = self.player.pos[0] + depth * np.cos(self.player.angle + FOV_angle)
        y = self.player.pos[1] + depth * np.sin(self.player.angle + FOV_angle)

        is_wall = self.map.is_in_region0((x, y), WALL)

        ind_wall = is_wall.argmax(axis=1) - 1
        ind_wall[np.logical_not(is_wall.any(axis=1))] = N_depth - 1

        for i_a, ind in enumerate(ind_wall):
            if ind >= 0:
                pygame.draw.line(self.map.surface, GREEN if FOV_angle[i_a]==0 else GREY,
                                 (x[i_a, 0]*MAP_SCALE, y[i_a, 0]*MAP_SCALE),
                                 (x[i_a, ind]*MAP_SCALE, y[i_a, ind]*MAP_SCALE))

                current_depth = depth[0, ind]*cos(FOV_angle[i_a])
                project_height = PROJ_COEFFICIENT/current_depth
                c = 255 / (1 + current_depth**2/2000)
                color = (c, c//2, c//3)
                pygame.draw.rect(self.surface, RED if FOV_angle[i_a]==0 else color,
                                 (i_a*SCALE, HALF_HEIGHT-project_height//2,
                                  SCALE, project_height))
