"""
DOCSTRING

The spawner is the object responsible for the invaders' spawning pattern.
In Java, I would probably have included its methods as static methods for 
the invader class.

The spawner works according to a specific pattern.
Once the game is initialized, it spawns more invaders than later (in this case, 4),
and then proceeds to spawn an increasing number of invaders. Importantly, the number
of invaders in the initial wave is different than the number of invaders in successive
waves. In later waves, the number of invaders only increases, and it doesn't decrease at
any point. 
"""

import random

from .constants import Win, Paths, Invader
from .space_invader import SpaceInvader

class Spawner():
    """
    Object responsible for spawning invaders.

    There are four attributes:
     - initial_invaders = the number of invaders spawned once the game is booted
     - later_invaders = the initial number of invaders spawned
                        after the first spawn
     - increment_time = the time  in seconds after which the number of 
                        spawning invaders increases by 1
                        (e.g. every interval=2 seconds, one extra invader 
                        spawns in each wave)
     - interval = the interval in seconds between each successive wave

    There are two main methods:
     - init_spawn is called only once at the beginning, and at once
       spawns a set number of invaders.
     - later_spawn is called later at a fixed interval, spawning an
       increasing number of invaders, again at set value
    """

    def __init__(
        self, 
        initial_invaders: int, 
        later_invaders: int,
        increment_time: int,
        interval: int,
    ):
        self.initial_invaders = initial_invaders
        self.later_invaders = later_invaders
        self.increment = 1 / increment_time # needed for later function
        self.interval = interval * Win.FPS.value

    def init_spawn(self) -> list:
        """
        First invader spawn, typically more than later spawns
        """
        return self._spawn(self.initial_invaders)

    def later_spawn(self, frame:int) -> list:
        """
        Spawns and increasing number of invaders.
        Every {interval} seconds, there is a new wave of invaders.
        Every time, the number of invaders increases by {increment},
        and the floor of that number is spawned.
        """
        # Spawns an increasing number of invaders.
        # Every time the function is called, an increment
        
        if frame % self.interval == 0:
            self.later_invaders += self.increment
            return self._spawn(int(self.later_invaders)) # Floor
        return []

    def _spawn(self, num_invaders: int) -> list:
        """
        Private helper method that spawns the invaders.
        By default it the invaders' initializing variable values are
        in the enums file.
        """
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
