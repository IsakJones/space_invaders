"""
DOCSTRING

This is the file for the bullet class.
"""

import pygame

from .constants import Bulletenum, Colors

class Bullet():
    def __init__(self, init_x: int, init_y: int):
        self.vel = Bulletenum.VEL.value
        self.rect = pygame.Rect(
           init_x,
           init_y,
           Bulletenum.WIDTH.value,
           Bulletenum.HEIGHT.value,
        )
        self.image = pygame.Surface(
            (Bulletenum.WIDTH.value, Bulletenum.HEIGHT.value)
        )
        self.image.fill(Colors.ORANGE.value)
    
    def travel(self):
        """
        Method must be called each clock tick!
        """
        self.rect.y -= self.vel

    def out_of_bounds(self) -> bool:
        """
        Returns true if past the screen.
        """
        return self.rect.y <= Bulletenum.CUTTOFF.value
    
    def get_rect(self) -> tuple:
        return (self.rect.x, self.rect.y)

    def get_y(self) -> int:
        return self.rect.y
    
    def get_x(self) -> int:
        return self.rect.x

    def get_image(self) -> pygame.Surface:
        return self.image

