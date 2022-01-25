"""
DOCSTRING

The game object handles the game logic. It starts the game by initializing
the main objects (i.e. the invaders, the spaceship etc.) as its own attributes. 
There is only one method, run. The Game object makes reference to every object in
the module except for the Menu object, the DB object, and the abstract classes.
It makes extensive use of the Window object to update the display.

All attributes' initializing variables are pulled from their respective "enum".
Changing initializing variables for testing should be done in the constats file.
"""

import pygame
import os

from .earth import Earth
from .sound import Sound
from .window import Window
from .spawner import Spawner
from .space_ship import SpaceShip
from .constants import Paths, Ship, Spawning, BASE_LIVES

class Game():

    def __init__(self, sound: Sound, screen: Window):
        # use sound and screen from menu
        self.sound = sound
        self.screen = screen
        # define player-controlled spaceship and spawner
        self.space_ship = SpaceShip(
            vel=Ship.VEL.value,
            lives=Ship.LIVES.value,
            init_x=Ship.INITX.value,
            init_y=Ship.INITY.value,
            width=Ship.WIDTH.value,
            height=Ship.HEIGHT.value,
            delay_hit=Ship.DELAYHIT.value,
            path=Paths.SHIP.value,
            sound=self.sound
        )
        self.spawner = Spawner(
            initial_invaders=Spawning.INIT.value,
            later_invaders=Spawning.LATER.value,
            increment_time=Spawning.INCREMENT.value,
            interval=Spawning.INTERVAL.value
        )
        # Spawn the invaders!
        self.invaders = self.spawner.init_spawn()
        self.earth = Earth(lives=BASE_LIVES)
        self.lasers = []
        self.score = 0

    def run(self) -> bool:
        """
        The main game app. Returns true if the game should restart.
        """
        # Play music
        self.sound.play_soundtrack()
        # Run the game
        run = True
        while run:
            # Check for quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
             
            # # check for game over
            if self.space_ship.is_destroyed() or self.earth.is_destroyed():
                return self.score
            # tick clock, update frame count
            self.screen.update_frame()
            self.screen.scroll()
            # spawn new invaders
            self.invaders.extend(
                self.spawner.later_spawn(self.screen.get_frame())
            )

            # check if any lasers are out of bounds
            # works because lasers are naturally sorted from highest to lowest
            # and player can at most shoot one laser per frame
            if self.lasers and self.lasers[0].out_of_bounds():
                del self.lasers[0]

            # check if a laser has hit an invader
            invaders_to_remove = set()
            lasers_to_remove = set()
            
            for laser in self.lasers:
                for invader in self.invaders:
                    if invader.is_hit(laser):
                        self.score += 100
                        invaders_to_remove.add(invader)
                        lasers_to_remove.add(laser)
            # remove invaders  
            for invader in invaders_to_remove:
                self.invaders.remove(invader)
            # remove lasers
            for laser in lasers_to_remove:
                self.lasers.remove(laser)

            # register pressed keys (left, right, and spacebar)
            keys_pressed = pygame.key.get_pressed()
            self.space_ship.move(keys_pressed)
            self.lasers.extend(self.space_ship.shoot(keys_pressed))
            # Update background
            self.screen.scroll()
            # Lasers
            for laser in self.lasers:
                laser.travel()
                self.screen.update_laser(laser)

            # Invaders
            for invader in self.invaders:
                # Update location
                self.screen.update_invader(invader)
                # Check if it's reached the base
                if self.earth.is_hit(invader):
                    self.earth.lose_life()
                    # print("An invader has reached your base!")
                    self.invaders.remove(invader)
                # Check if it's run against the ship
                if self.space_ship.is_hit(self.screen.get_frame(), invader):
                    self.space_ship.lose_life()
                    # print(f"The ship still has {self.space_ship.get_lives()} lives.")
                    self.invaders.remove(invader)

            # Only display the ship if it has full health
            if not self.space_ship.is_destroyed():
                self.screen.update_ship(self.space_ship)
            # Display health and score
            self.screen.health(self.space_ship, self.earth)
            self.screen.score(self.score)
            # Update the screen
            self.screen.update()

