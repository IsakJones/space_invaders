"""
DOCSTRING

Includes abstract classes for Base, SpaceShip and SpaceInvader.

Thing only includes lives, as all three classes above have them.
Creature handles more attributes for visual objects such as SpaceShip and SpaceInvader.
"""

import pygame
import os

class Thing():
    """
    Abstract class shared by Base, SpaceShip and SpaceInvader.
    Only includes lives attribute and related methods.
    """
    def __init__(self, lives: int):
        self.lives = lives

    def lose_life(self):
        self.lives -= 1

    def acquire_life(self):
        self.lives += 1

    def get_lives(self) -> int:
        return self.lives

    def is_destroyed(self) -> bool:
        return self.lives <= 0

class Creature(Thing):
    """
    Abstract class shared by SpaceShip and SpaceInvader.
    """
    def __init__(
        self,
        vel: int, # velocity
        lives: int,
        init_x: int, # X coordinate of the initial location
        init_y: int, # Y coordinate of the initial location
        width: int, 
        height: int, # dimensions
        path: os.path # path to the image
    ): 
        super().__init__(lives)
        self.vel = vel
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(
            pygame.image.load(path), 
            (width, height)
        ).convert_alpha() # needed for transparency
        self.rect = pygame.Rect(
            init_x,
            init_y,
            width,
            height
        )

    def get_rect(self) -> tuple:
        return (self.rect.x, self.rect.y)
    
    def get_image(self) -> pygame.image:
        return self.image

    

    