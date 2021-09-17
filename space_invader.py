import random
import pygame
import os

from enums import Win
from creature import Creature

class SpaceInvader(Creature):
    def __init__(self,
                 vel: int,
                 lives: int,
                 init_x: int, 
                 init_y: int, 
                 width: int,
                 height: int,
                 path: os.path):
        
        super().__init__(vel, init_x, init_y, width, height, path)
        
        self.right = random.choice([True, False]) # Does it initially move right?
        self.switch_time = int(60 * (1 + random.uniform(0, 1)))
        
    def move(self, frame: int) -> None:
        # The invader changes direction every one / two seconds
        frame = frame % self.switch_time
        condition_left = 0 <= self.rect.x <= 1
        condition_right = 0 <= self.rect.x - Win.WIDTH.value + self.width <= 1
        # If the invader is out of bounds, or one/two seconds have past
        if frame == 0 or condition_left or condition_right:
            self.right = not self.right # change direction
        
        # Move
        if self.right:
            self.rect.x += self.vel # RIGHT
        else:
            self.rect.x -= self.vel # LEFT
        self.rect.y += self.vel - 1 # DOWN

