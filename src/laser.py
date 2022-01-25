"""
DOCSTRING

This is the file for the laser class, which has no inheritance.
"""

import pygame

from .constants import Laserconst

class Laser():
    def __init__(self, init_x: int, init_y: int, image: pygame.Surface):
        self.vel = Laserconst.VEL.value
        self.image = image
        self.rect = pygame.Rect(
           init_x,
           init_y,
           Laserconst.WIDTH.value,
           Laserconst.HEIGHT.value,
        )
    
    def travel(self):
        """
        Method must be called each clock tick!
        """
        self.rect.y -= self.vel

    def out_of_bounds(self) -> bool:
        """
        Returns true if past the screen.
        """
        return self.rect.y <= Laserconst.CUTTOFF.value
    
    def get_rect(self) -> tuple:
        return (self.rect.x, self.rect.y)

    def get_y(self) -> int:
        return self.rect.y
    
    def get_x(self) -> int:
        return self.rect.x

    def get_image(self) -> pygame.Surface:
        return self.image

