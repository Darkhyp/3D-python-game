import pygame

from doom_py.CONFIGS import TILE_X, TILE_Y


class Sprite:
    def __init__(self):
        self.sprites = {
            'barrel': pygame.image.load('doom/sprites/barrel.jpg').convert_alpha()
        }
        self.list_of_objects = [
            SpriteObject(self.sprites['barrel'], True, (7.1, 2.1), 1.8, 0.4 ),
            SpriteObject(self.sprites['barrel'], True, (5.9, 2.1), 1.8, 0.4),
        ]


class SpriteObject:
    def __init__(self, object, is_static, pos, h_shift, scale):
        self.object = object
        self.is_static = is_static
        self.pos = pos[0]*TILE_X, pos[1]*TILE_Y
        self.h_shift = h_shift
        self.scale = scale

    def locate_object(self, player, map):
        pass
