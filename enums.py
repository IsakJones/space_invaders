"""
DOCSTRING

Contains constants in the form of enums. 
Enum buckets are:

 - Paths (for assets)
 - Colors
 - Win (pixel dimensions for the window)
 - Ship (pixel dimensions, initial location, and velocity for the spaceship)
 - Invader (pixel dimensions and initial location for the invader)
 
"""
import os
from enum import Enum

class Paths(Enum):
    BACKGROUND = os.path.join("Assets", "background.png")
    MUSIC = os.path.join("Assets", "soundtrack.mp3")
    SHIP = os.path.join("Assets", "space_ship.png")
    INVADER = [
        os.path.join("Assets", "orange_invader.png"),
        os.path.join("Assets", "green_invader.png"),
        os.path.join("Assets", "yellow_invader.png"),
        os.path.join("Assets", "fucsia_invader.png"),
    ]

class Colors(Enum):
    WHITE = (255, 255, 255)
    PURPLE = (64, 0, 64)
    BLACK = (0, 0, 0)

class Win(Enum):
    WIDTH = 640 # = 256 * 2.5
    HEIGHT = 560 # = 224 * 2.5
    FPS = 60

class Ship(Enum):
    VEL = 4 # velocity
    LIVES = 1
    INITX = 320 - 25 # The middle of the window
    INITY = 460
    WIDTH = 50
    HEIGHT = 50

class Invader(Enum):
    VEL = 2 # velocity
    LIVES = 1
    INITX = 320 - 15 # The middle of the window
    INITY = -30
    WIDTH = 52 # 575 / 11 
    HEIGHT = 38 # 420 / 11

class Spawning(Enum):
    INIT = 4
    LATER = 2
    INTERVAL = 120 # Number of frames that 

    