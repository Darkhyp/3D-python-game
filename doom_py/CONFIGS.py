# doom parameters

# display
from math import pi, tan

from pygame import K_w, K_p, K_s, K_a, K_d, K_LEFT, K_RIGHT

DISPLAY_WIDTH  = 1200
DISPLAY_HEIGHT = 800
HALF_WIDTH  = DISPLAY_WIDTH/2
HALF_HEIGHT = DISPLAY_HEIGHT/2

# display background
BACKGROUND_COLOR = (0, 30, 0)

WHITE = (255, 255, 255)
GREY = (120, 120, 120)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 50, 0)
BLUE = (0, 0, 255)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (120, 120, 0)


# FPS = 60
FPS = 120

# player keys
PLAYER_UP = K_w
PLAYER_DOWN = K_s
PLAYER_LEFT = K_a
PLAYER_RIGHT = K_d
PLAYER_TURN_LEFT = K_LEFT
PLAYER_TURN_RIGHT = K_RIGHT

# player
PLAYER_RADIUS = 12
ANGLE_STEP = 0.02

# map
N_COLS = 13 # ix-axis
N_ROWS = 12 # iy-axis
WALL = 1
MAP_SCALE = 0.2
MAP_POS = (0, 0)    # left-top corner
TILE_X = 100
TILE_Y = 60
MAP_WIDTH       = TILE_X * N_COLS
MAP_HEIGHT      = TILE_Y * N_ROWS
MAP_HALF_WIDTH  = MAP_WIDTH /2
MAP_HALF_HEIGHT = MAP_HEIGHT /2
MAP_TILE_X      = TILE_X * MAP_SCALE
MAP_TILE_Y      = TILE_Y * MAP_SCALE

# pause key
PAUSE_KEY = K_p

# ray parameters
# field of view
FOV = pi/3
HALF_FOV = FOV/2
# CENTER_RAY = 10
CENTER_RAY = 60
# CENTER_RAY = 150
N_RAYS = CENTER_RAY*2 + 1
MAX_DEPTH = 800
# MAX_DEPTH = 1200
DELTA_FOV = FOV/N_RAYS
DISTANCE = N_RAYS / (2*tan(HALF_FOV))
PROJ_COEFFICIENT = 3 * DISTANCE * TILE_X
SCALE = DISPLAY_WIDTH // (N_RAYS-1)


## textures with the size (TEXTURE_WIDHT, TEXTURE_HEIGHT) = (1200, 1200)
FLOOR_IMAGE = r'doom_py\images\2.png'
WALL_IMAGE = r'doom_py\images\1.png'
SKY_IMAGE = r'doom_py\images\sky.png'
TEXTURE_WIDHT = 1200
TEXTURE_HEIGHT = 1200
TILE = max(TILE_X, TILE_Y)
TEXTURE_SCALE = TEXTURE_WIDHT // TILE


# math
DOUBLE_PI = 2*pi
