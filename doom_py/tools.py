import pygame
import numpy as np

from doom_py.CONFIGS import TILE_X, TILE_Y, MAX_DEPTH


def gradientRect( window, leftbottom_colour, righttop_colour, target_rect, is_vertical=True ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    if is_vertical:
        pygame.draw.line(colour_rect, leftbottom_colour, (0, 1), (1, 1))  # bottom colour line
        pygame.draw.line(colour_rect, righttop_colour, (0, 0), (1, 0))  # top colour line
    else:
        pygame.draw.line( colour_rect, leftbottom_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
        pygame.draw.line( colour_rect, righttop_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )                                    # paint it



def to_index(pos):
    return np.int8(pos[0]//TILE_X), np.int8(pos[1]//TILE_Y)


def mapping(pos):
    return int(pos[0]//TILE_X), int(pos[1]//TILE_Y)

# check verticals/horizontals
def check_intersection(x0, y0, ind0, ind1, step, coef1, coef2, is_in_region):
    inc = 1 if coef1 > 0 else -1
    x = np.arange(ind0 + 1 if inc > 0 else ind0, ind1 + inc, inc) * step
    if coef1 != 0:
        depth = (x - x0) / coef1
        y = y0 + depth * coef2

        is_wall = is_in_region(x, y)
        if len(is_wall) > 0:
            if is_wall.any():
                ind_wall = is_wall.argmax()
            else:
                ind_wall = len(is_wall)-1
            return x[ind_wall], y[ind_wall], depth[ind_wall]
        else:
            return x0 + MAX_DEPTH * coef1, y0 + MAX_DEPTH * coef2, MAX_DEPTH
    else:
        return x0, y0 + inc*MAX_DEPTH, MAX_DEPTH

