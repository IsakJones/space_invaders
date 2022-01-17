"""
DOCSTRING

The game object handles the flow of the game and everything that isn't handled by
another dedicated object. Hence is starts the game, with the main objects (i.e. the
screen, the invaders, the spaceship etc.) as its own attributes. Methods handle sound
effects, which I didn't feel needed a dedicated object, and the flow of the game over
screen.

All attributes' initializing variables are pulled from their respective enum.
Changing initializing variables for the sake of testing should be done in the enums file.
"""

import pygame
import os

from .base import Base
from .sound import Sound
from .window import Window
from .spawner import Spawner
from .space_ship import SpaceShip
from .constants import Win, Paths, Ship, Spawning, BASE_LIVES

class Game():

    def __init__(self):
        pygame.init()

        self.sound = Sound(
            soundtrack=Paths.SOUNDTRACK.value,
            game_over=Paths.GAME_OVER.value,
            laser=Paths.LASER_SOUND.value
        )
        self.screen = Window(
            fps=Win.FPS.value,
            font=Paths.FONT.value,
            width=Win.WIDTH.value,
            height=Win.HEIGHT.value,
            background=Paths.BACKGROUND.value
        )
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
        self.lasers = []
        self.base = Base(lives=BASE_LIVES)
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
            if self.space_ship.is_destroyed() or self.base.is_destroyed():
                return self.game_over()
            # tick clock, update frame count
            self.screen.update_frame()
            self.screen.scroll()
            # spawn new invaders
            self.invaders.extend(
                self.spawner.later_spawn(self.screen.get_frame())
            )

            # check if any lasers are out of bounds
            # works because lasers are naturally sorted from highest to lowest
            while self.lasers and self.lasers[0].out_of_bounds():
                self.lasers = self.lasers[1:]

            # check if a laserjhas hit an invader
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
                if self.base.is_hit(invader):
                    self.base.lose_life()
                    # print("An invader has reached your base!")
                    self.invaders.remove(invader)
                # Check if it's run against the ship
                if self.space_ship.is_hit(self.screen.get_frame(), invader):
                    self.space_ship.lose_life()
                    # print(f"The ship still has {self.space_ship.get_lives()} lives.")
                    self.invaders.remove(invader)

            # Ship
            if not self.space_ship.is_destroyed():
                self.screen.update_ship(self.space_ship)
            # Display health and score
            self.screen.health(self.space_ship, self.base)
            self.screen.score(self.score)
            # If it's the start, display the title
            self.screen.title()
            # Update the screen
            self.screen.update()

    def game_over(self):
        """
        Handles game over. Calls game over screen in window, changes music,
        and supports the iterative restart in the main file.
        Returns true if the game should restart.
        """
        # Stop music and play sound
        self.sound.play_game_over()
        
        while True:
            # Check for r press
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_q:
                        return False
            # Update screen
            self.screen.game_over()
            self.screen.update_frame(fps=15)
