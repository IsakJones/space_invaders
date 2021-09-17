import pygame
import os


from space_ship import SpaceShip
from enums import Colors, Ship, Invader
from space_invader import SpaceInvader


class Background(pygame.sprite.Sprite): # Look up what this means!
    def __init__(self, path: os.path):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(path)
        self.height = self.image.get_height() 
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0, 0)
        # The next attributes  are necessary for rotation
        self.rotation = 270
        self.rotated = pygame.transform.rotate(self.image, self.rotation)

    def rect_desc(self, num: int) -> tuple:
        # The background is displayed lower by num, higher if num<0
        return (self.rect.left, self.rect.top-num)
    
    def rotate(self) -> None:
        # rotate self.image and self.rotated by 270 degrees
        self.image = self.rotated
        self.rotated = pygame.transform.rotate(self.image, self.rotation)

    
class Window():
    def __init__(self, width: int, height: int, caption: str, path: os.path):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.background = Background(path)

    def fill_black(self) -> None:
        # Fills the background with black, just in case.
        self.win.fill(Colors.BLACK.value)

    def update(self) -> None:
        # Updates the whole screen, necessary for each frame
        pygame.display.update()

    def scroll(self, frame: int) -> None:
        """
        Adds backgorund image and infinite scrolling.
        Once the background is scrolled over (i.e. once the original image's 
        lower limit has risen above the window's lower side) the same image
        rises below it, rotated by 270 degrees.
        """
        # Adds background image and infinite scrolling
        frame = frame % self.background.height
        # If the old background has been completely scrolled over, 
        # make the old background the new background
        if frame == 0:
            self.background.rotate()
        # Display the old background
        self.win.blit(self.background.image, self.background.rect_desc(frame))
        # If the old background's lower limit has risen above the
        # window's lowest side, make a rotated background rise below it
        if frame > self.background.height-self.height:
            offset = frame - self.background.height
            self.win.blit(
                self.background.rotated,
                self.background.rect_desc(offset)
            )

    def update_ship(self, ship: SpaceShip, keys_pressed) -> None:
        # Updates the location of the ship
        ship.move(keys_pressed)
        self.win.blit(ship.get_image(), ship.get_rect())

    def update_invaders(self, frame: int, ship: SpaceShip, invaders: list) -> None:
        # Updates the location of the invader
        for invader in invaders:
            if invader.rect.y > Ship.INITY.value - Invader.WIDTH.value:
                ship.death(invader)
            invader.move(frame)
            self.win.blit(invader.get_image(), invader.get_rect())




        