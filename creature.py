import pygame
import os

class Creature():
    # Abstract class for SpaceShip and Invader objects
    def __init__(self,
                 vel: int,
                 init_x: int, # X coordinate of the initial location
                 init_y: int, # Y coordinate of the initial location
                 width: int, 
                 height: int, 
                 path: os.path): # path to the image

        self.vel = vel
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(
            pygame.image.load(path), (width, height)
        ).convert_alpha()
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

    

    