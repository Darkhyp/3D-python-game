import timeit
from math import cos, sqrt
import numpy as np

import pygame
from numpy.ma import sin

from doom_py.CONFIGS import *


class Player:
    def __init__(self, surface, map, pos, angle, speed):
        self.surface = surface
        self.map = map
        self.x, self.y = pos
        self.angle = angle
        self.speed = speed

        self.mouse_position = pygame.mouse.get_pos()

    @property
    def pos(self):
        return self.x, self.y

    def movement(self):
        keys = pygame.key.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        x = self.pos[0]
        y = self.pos[1]
        step_x = self.speed*cos(self.angle)
        step_y = self.speed*sin(self.angle)
        if keys[PLAYER_UP]:
            x += step_x
            y += step_y
        if keys[PLAYER_DOWN]:
            x -= step_x
            y -= step_y
        if keys[PLAYER_LEFT]:
            x += step_y
            y -= step_x
        if keys[PLAYER_RIGHT]:
            x -= step_y
            y += step_x
        if not self.map.is_in_region((x, y), WALL):
            self.x = x
            self.y = y

        if keys[PLAYER_TURN_LEFT] or mouse_position[0] < self.mouse_position[0] or mouse_position[0] == 0:
            self.angle -= ANGLE_STEP
            self.mouse_position = mouse_position
        if keys[PLAYER_TURN_RIGHT] or mouse_position[0] > self.mouse_position[0] or mouse_position[0] == DISPLAY_WIDTH-1:
            self.angle += ANGLE_STEP
            self.mouse_position = mouse_position


