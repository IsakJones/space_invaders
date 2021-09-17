"""
Spawns invaders
"""
import random
import os

from enums import Win, Paths, Invader
from space_invader import SpaceInvader

class Spawner():
    def __init__(self, initial: int, later: int):
        self.initial = initial # Invaders spawning initially
        self.later = later # Invaders spawning after the first time

    def init_spawn(self) -> list:
        return self._spawn(self.initial)

    def later_spawn(self) -> list:
        return self._spawn(self.later)

    def _spawn(self, num_invaders: int) -> list:
        # returns a list of spawning invaders!
        invaders = []
        # half_width = Win.WIDTH.value // 2
        for i in range(num_invaders):
            spawn_x = random.randint(0, Win.WIDTH.value-Invader.WIDTH.value)
            spawn_y = -random.randint(Invader.WIDTH.value, Invader.WIDTH.value * 2)
    
            invaders.append(
                SpaceInvader(
                    Invader.VEL.value,
                    Invader.LIVES.value,
                    spawn_x,
                    spawn_y,
                    Invader.WIDTH.value,
                    Invader.HEIGHT.value,
                    random.choice(Paths.INVADER.value)
                )
            )
        return invaders

   
