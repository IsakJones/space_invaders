"""
DOCSTRING

Object reppresenting the terrifying space invaders!
Just like creature, but with custom motion that 
constantly points downwards with randomized swerving.
"""

import random
import os

from .constants import Win
from .laser import Laser
from .abstract import Creature

class SpaceInvader(Creature):

    def __init__(
        self,
        vel: int,
        lives: int,
        init_x:  int,
        init_y:  int,
        width: int,
        height: int,
        path: os.path
    ):
        super().__init__(vel, lives, init_x, init_y, width, height, path)
        # self.direction is true if the invader swerves right, false if it swerves left
        self.direction = random.choice([True, False]) 
        # the swerve direction switches every 1 to 2 seconds
        self.switch_time = int(Win.FPS.value * (1 + random.uniform(0, 1)))

    def move(self, frame: int) -> None:
        """
        method called in each frame updating the location of the invader.
        The invader always moves downward, and switches left / right direction
        according to self.switch_time, and also whether it bumps against one of
        the walls. Condition left and right are true if it bumps against either.
        """
        frame = frame % self.switch_time
        # If the invader is too far right, swerve left
        if 0 <= self.rect.x - Win.WIDTH.value + self.rect.width <= self.vel-1:
            self.direction = False
        # If the invader is too far left, swerve right
        if 0 <= self.rect.x <= self.vel-1:
            self.direction = True
        # Each switch time, change direction
        elif frame == 0:
            self.direction = not self.direction 
        # Move
        if self.direction:
            self.rect.x += self.vel # RIGHT
        else:
            self.rect.x -= self.vel # LEFT
        self.rect.y += self.vel - 1 # DOWN

    def is_hit(self, laser: Laser) -> bool:
        """
        Returns true if the laser has hit the invader.
        """
        return self.rect.colliderect(laser.rect)
