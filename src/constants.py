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
    MENU_SOUNDTRACK = os.path.join("assets", "menu.wav")
    BACKGROUND = os.path.join("assets", "background.png")
    SOUNDTRACK = os.path.join("assets", "soundtrack.wav")
    GAME_OVER = os.path.join("assets", "game_over.wav")
    SHIP = os.path.join("assets", "space_ship.png")
    EARTH = os.path.join("assets", "earth.png")
    MENU = os.path.join("assets", "menu.wav")
    FONT = os.path.join("assets", "arcade.TTF")
    HEART = os.path.join("assets", "heart.png")
    TITLE = os.path.join("assets", "title.png")
    LASER_IMAGE = os.path.join("assets", "laser.png")
    LASER_SOUND = os.path.join("assets", "laser.wav")
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
    WIDTH = 640 
    HEIGHT = 600 

class Titles(Enum):
    TITLE_SIZE = 60
    TITLE_HEIGHT = 100 # Win.HEIGHT * 0.25
    SUB_HEIGHT = 150 # TITLE_HEIGHT + 60 + 10
    SUB_SIZE = 30

class Health(Enum):
    HEIGHT = 32 # 105 / 3, also the side of the square castle
    WIDTH = 40 # 130 / 3
    SPACING = 6
    Y = 6 

class Score(Enum):
    SIZE = 40
    PADDING = 6

class Buttons(Enum):
    SIZE = 50
    RET_SIZE = 37 # ~ 3/4 * 50
    RET_X = 30
    RET_Y = 540
    FIRST_Y = 300
    SPACING = 60 # size + 10

class Table(Enum):
    SIZE = 35
    FIRST_Y = 200
    SPACING = 43
    PADDING = 70

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

class Laserconst(Enum):
    VEL = 6
    WIDTH = 6
    HEIGHT = 30
    CUTTOFF = -15 # The height, but negative

BASE_LIVES = 3