"""
DOCSTRING

Contains main initializing variables as constants.
Changing initializing variables for testing should be done here.

While verbose, the python enum syntax supports the project's
overarching object-oriented approach and keeps all variables
in one single module. 

Enum buckets are:
 - Paths (for assets, such as images and sounds)
 - Colors (only white is used)
 - Win (__init__ values for the window)
 - Ship (__init__ values for the ship)
 - Invader (__init__ values for the invader)
 - Spawning (__init__ values for the spawner)
 - Health (determines size and location of health icons)
 - Text (size and location of title and game over texts)

Lastly, the Base object only has one attribute, hence it has
a constant variable instead of an enum object.
"""

import os
from enum import Enum

class Paths(Enum):
    BACKGROUND = os.path.join("assets", "background.png")
    SOUNDTRACK = os.path.join("assets", "soundtrack.wav")
    GAME_OVER = os.path.join("assets", "game_over.wav")
    CASTLE = os.path.join("assets", "castle_grey.png")
    SHIP = os.path.join("assets", "space_ship.png")
    FONT = os.path.join("assets", "arcade.TTF")
    HEART = os.path.join("assets", "heart.png")
    TITLE = os.path.join("assets", "title.png")
    LASER = os.path.join("assets", "laser.wav")
    INVADER = [
        os.path.join("assets", "blue_invader.png"),
        os.path.join("assets", "green_invader.png"),
        os.path.join("assets", "fucsia_invader.png"),
        os.path.join("assets", "orange_invader.png"),
        os.path.join("assets", "yellow_invader.png"),
    ]

class Colors(Enum):
    WHITE = (255, 255, 255)
    ORANGE = (255, 165, 0)
    BLACK = (0, 0, 0)

class Win(Enum):
    FPS = 60
    WIDTH = 640 # = 256 * 2.5
    HEIGHT = 560 # = 224 * 2.5

class Text(Enum):
    TITLE_TEXT = "Space Invaders"
    GAME_OVER_TEXT = "Game Over"
    SUB_ONE_TEXT = "Press R to restart"
    SUB_TWO_TEXT = "Press Q to quit"
    TITLE_TIME = 120
    TITLE_SIZE = 60
    TITLE_HEIGHT = 1/4 # relative to height
    SUB_SIZE = 30
    SUB_HEIGHT_ONE = 0.7 # ^^

class Health(Enum):
    HEIGHT = 32 # 105 / 3, also the side of the square castle
    HEART_WIDTH = 40 # 130 / 3
    HEART_SPACING = 6
    CASTLE_SPACING = 14 # = 40 + 6 - 32
    Y = 6 

class Ship(Enum):
    VEL = 5 # velocity
    LIVES = 3
    INITX = 320 - 25 # The middle of the window
    INITY = 460
    WIDTH = 50
    HEIGHT = 50
    DELAYHIT = 1 # in seconds

class Invader(Enum):
    VEL = 2 # velocity
    LIVES = 1
    INITX = 320 - 15 # The middle of the window
    INITY = -30
    WIDTH = 48 # 575 / 11 
    HEIGHT = 35 # 420 / 11

class Spawning(Enum):
    INIT = 4
    LATER = 2
    INTERVAL = 2 # new wave every 2 seconds
    INCREMENT = 4 # extra invader every 10 seconds

class Bulletenum(Enum):
    VEL = 6
    WIDTH = 6
    HEIGHT = 15
    CUTTOFF = -15 # The height, but negative

BASE_LIVES = 3