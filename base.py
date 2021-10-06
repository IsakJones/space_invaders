"""
DOCSTRING

The unseen base that the ship is defending from the space invaders.
Only has an attribute with the number of lives, but adds a 
method returning true if a spaceinvader makes it past the ship.
It's lives are represented in the game with the castle icons.
"""

from enums import Win
from abstract import Thing
from space_invader import SpaceInvader

class Base(Thing):

    def __init__(self, lives: int):
        super().__init__(lives)

    def is_hit(self, invader: SpaceInvader):
        return invader.get_rect()[1] > Win.HEIGHT.value # i.e. the y location
