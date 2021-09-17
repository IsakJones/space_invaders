import pygame
import os

from creature import Creature
from enums import Win, Ship, Invader
from space_invader import SpaceInvader

class SpaceShip(Creature):
    def __init__(self,
                 vel: int,
                 lives: int,
                 init_x: int, 
                 init_y: int, 
                 width: int,
                 height: int,
                 path: os.path):

        super().__init__(vel, init_x, init_y, width, height, path)

    def move(self, keys_pressed: dict) -> None:
        # Updates location
        condition = self.rect.x < Win.WIDTH.value-self.width

        if keys_pressed[pygame.K_LEFT] and self.rect.x > 0: # LEFT
            self.rect.x -= self.vel
        if keys_pressed[pygame.K_RIGHT] and condition: # RIGHT
            self.rect.x += self.vel

    def death(self, invader: SpaceInvader) -> bool:
        # returns true if an invader kills the ship!
        # The following is if the invader is above the ship
        touching_up = self.rect.y - invader.rect.y < Invader.HEIGHT.value
        touching_down = invader.rect.y - self.rect.y < Ship.HEIGHT.value
        # If the invader is left of the ship
        touching_left = self.rect.x - invader.rect.x < Invader.WIDTH.value
        touching_right = invader.rect.x - self.rect.x < Ship.WIDTH.value
        # complicated condition
        if (touching_up or touching_down) and (touching_left or touching_right):
            print("Dead!")
            print("Hello!")
            # TODO check
