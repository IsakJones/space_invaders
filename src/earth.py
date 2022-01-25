"""
DOCSTRING

The unseen earth that the ship is defending from the space invaders.
Only has an attribute with the number of lives, but adds a 
method returning true if a spaceinvader makes it past the ship.
Its lives are represented in the game with the planet icons.
"""

from .constants import Win
from .abstract import Thing
from .space_invader import SpaceInvader

class Earth(Thing):

    def __init__(self, lives: int):
        super().__init__(lives)

    def is_hit(self, invader: SpaceInvader):
        return invader.get_rect()[1] > Win.HEIGHT.value # i.e. the y location
