"""
DOCSTRING

Object reppresenting the terrifying space invaders!
Just like creature, but with custom motion that 
constantly points downwards with randomized swerving.
"""

import random
import os

from enums import Win
from bullet import Bullet
from abstract import Creature

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
        # self.right is true if the invader swerves right, false if it swerves left
        self.right = random.choice([True, False]) 
        # the swerve direction switches every 1 to 2 seconds
        self.switch_time = int(Win.FPS.value * (1 + random.uniform(0, 1)))

    def move(self, frame: int) -> None:
        """
        Method called in each frame updating the location of the invader.
        The invader always moves downward, and switches left / right direction
        according to self.switch_time, and also whether it bumps against one of
        the walls. Condition left and right are true if it bumps against either.
        """
        frame = frame % self.switch_time
        # self.vel-1, otherwise it might speed past the border 
        condition_left = 0 <= self.rect.x <= self.vel-1
        condition_right = 0 <= self.rect.x - Win.WIDTH.value + self.width <= self.vel-1
        # If the invader is out of bounds, or one/two seconds have past
        if frame == 0 or condition_left or condition_right:
            self.right = not self.right # change direction
        # Move
        if self.right:
            self.rect.x += self.vel # RIGHT
        else:
            self.rect.x -= self.vel # LEFT
        self.rect.y += self.vel - 1 # DOW

    def is_hit(self, bullet: Bullet) -> bool:
        """
        Returns true if the bullet has hit the invader.
        """
        return self.rect.colliderect(bullet.rect)
