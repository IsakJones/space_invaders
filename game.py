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

from base import Base
from window import Window
from bullet import Bullet
from spawner import Spawner
from space_ship import SpaceShip
from enums import Bulletenum, Win, Paths, Ship, Spawning, BASE_LIVES

class Game():

    def __init__(self):
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
            delay_shoot=Ship.DELAYSHOOT.value,
            path=Paths.SHIP.value
        )
        self.spawner = Spawner(
            initial_invaders=Spawning.INIT.value,
            later_invaders=Spawning.LATER.value,
            increment_time=Spawning.INCREMENT.value,
            interval=Spawning.INTERVAL.value
        )
        # Spawn the invaders!
        self.invaders = self.spawner.init_spawn()
        self.bullets = []
        self.base = Base(lives=BASE_LIVES)

    def run(self) -> bool:
        """
        The main game app. Returns true if the game should restart.
        """
        pygame.init()
        # Play music
        self.play_music()
        # Run the game
        run = True
        while run:
            # Check for quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
             
            # # check for game over
            # if self.space_ship.is_destroyed() or self.base.is_destroyed():
            #     return self.game_over()
            # tick clock, update frame count
            self.screen.update_frame()
            self.screen.scroll()
            # spawn new invaders
            self.invaders.extend(
                self.spawner.later_spawn(self.screen.get_frame())
            )
            # check if a bullet has hit an invader
            bullets_to_remove = set()
            invaders_to_remove = set()
            
            for bullet in self.bullets:
                # check if bullets out of the screen
                if bullet.out_of_bounds():
                    bullets_to_remove.add(bullet)
                for invader in self.invaders:
                    if invader.is_hit(bullet):
                        invaders_to_remove.add(invader)
                        bullets_to_remove.add(bullet)
            # remove invaders  
            for invader in invaders_to_remove:
                self.invaders.remove(invader)
            # remove bullets
            for bullet in bullets_to_remove:
                self.bullets.remove(bullet)

            # register pressed keys (left or right)
            keys_pressed = pygame.key.get_pressed()
            self.space_ship.move(keys_pressed)
            self.bullets.extend(self.space_ship.shoot(self.screen.get_frame(), keys_pressed))
            # Update background
            self.screen.scroll()
            # Ship
            self.screen.update_ship(self.space_ship)
            # Bullets
            for bullet in self.bullets:
                bullet.travel()
                self.screen.update_bullet(bullet)

            # Invaders
            for invader in self.invaders:
                # Update location
                self.screen.update_invader(invader)
                # Check if it's reached the base
                if self.base.is_hit(invader):
                    self.base.lose_life()
                    print("An invader has reached your base!")
                    self.invaders.remove(invader)
                # Check if it's run against the ship
                if self.space_ship.is_hit(self.screen.get_frame(), invader):
                    self.space_ship.lose_life()
                    print(f"The ship still has {self.space_ship.get_lives()} lives.")
                    self.invaders.remove(invader)
            # Display health
            self.screen.health(self.space_ship, self.base)
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
        self.stop_music()
        self.play_music(Paths.GAME_OVER.value, times=1)
        
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

    def play_music(self, path: os.path="/", times: int=-1):
        """
        Plays music at path {times} times. Default is "soundtrack.mp3".
        """
        path = Paths.MUSIC.value if path == "/" else path
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(times) # -1 is infinite loop

    def stop_music(self):
        """
        Stops the music.
        """
        pygame.mixer.music.stop()
