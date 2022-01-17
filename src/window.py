"""
DOCSTRING

This file includes all objects handling visual changes.

The Background object is necessary for the custom scrolling, and only used for that.
In fact, only the Window object calls it, hence I've included them in the same file.

The Window object handles all surfaces on display. It also handles the clock, which 
dictates the game's pace, and includes an attribute tracking the frame number, which is
important for many methods. The background, hearts, and earth icons are also attributes.
"""
import pygame
import os

from .base import Base
from .laser import Laser
from .space_ship import SpaceShip
from .constants import Paths, Colors, Text, Win, Health, Score
from .space_invader import SpaceInvader


class Background(): 

    def __init__(self, path: os.path): 
        self.image = pygame.image.load(path)
        self.height = self.image.get_height() 
        self.rect = self.image.get_rect()

    def rect_desc(self, num: int) -> tuple:
        # The background is displayed lower by num, higher if num<0
        return (self.rect.left, self.rect.top-num)
    
    
class Window():
    def __init__(
        self,
        fps: int,
        width: int, 
        height: int, 
        font: os.path,
        background: os.path
    ):
        self.fps = fps
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))
        self.background = Background(background)
        self.font  = font
        self.clock = pygame.time.Clock()
        self.frame = 0 # The current nth frame.
        self.score_font = pygame.font.Font(
            Paths.FONT.value,
            Score.SIZE.value
        )
        self.heart = pygame.transform.scale(
            pygame.image.load(Paths.HEART.value),
            (Health.WIDTH.value, Health.HEIGHT.value)
        )
        self.earth = pygame.transform.scale(
            pygame.image.load(Paths.EARTH.value),
            (Health.HEIGHT.value, Health.HEIGHT.value)
        )
        pygame.display.set_caption("Space Invaders!")

    def scroll(self) -> None:
        """
        Adds backgorund image and infinite scrolling.
        """
        frame = self.frame % self.background.height
        # Represent the background shifted down according to frame
        self.win.blit(self.background.image, self.background.rect_desc(frame))
        # Blit a second background underneath the current one if the
        # current one's lower border has shifted above the visible screen
        if frame > self.background.height-self.height:
            offset = frame - self.background.height
            self.win.blit(
                self.background.image,
                self.background.rect_desc(offset)
            )

    def title(self) -> None:
        """
        Displays the title according to the title_time in Text.
        """
        if self.frame > Text.TITLE_TIME.value:
            return None

        title_text = pygame.font.Font(
            Paths.FONT.value,
            Text.TITLE_SIZE.value
        ).render(Text.TITLE_TEXT.value, 1, Colors.WHITE.value)
        title_x = Win.WIDTH.value//2 - title_text.get_width()//2
        title_y = int(Win.HEIGHT.value * Text.TITLE_HEIGHT.value)

        self.win.blit(
            title_text,
            (title_x, title_y)
        )

    def health(self, space_ship: SpaceShip, base: Base) -> None:
        """
        Displays the health count for both the ship and the base.
        """
        # Display ship health
        for life in range(space_ship.get_lives()):
            heart_x = Health.SPACING.value * (life+1) + Health.WIDTH.value * life
            self.win.blit(
                self.heart,
                (heart_x, Health.Y.value)
            )
        # Display base health
        for life in range(base.get_lives()):
            earth_x = Health.SPACING.value * (life+1) + Health.HEIGHT.value * (life+1)
            # the HEIGHT is also the earth's side
            self.win.blit(
                self.earth,
                (Win.WIDTH.value - earth_x, Health.Y.value)
            )
    
    def score(self, score: int) -> None:
        """
        Displays score under the ship.
        """
        score_text = self.score_font.render(str(score), 1, Colors.WHITE.value)
        score_x = Win.WIDTH.value//2 - score_text.get_width()//2 - Score.PADDING.value
        score_y = Win.HEIGHT.value - score_text.get_height() - Score.PADDING.value
        
        self.win.blit(
            score_text,
            (score_x, score_y)
        )

    def game_over(self) -> None:
        """
        Handles the game over screen. Renders the associated texts 
        and displays them.
        """
        # Title info
        game_over_text = pygame.font.Font(
            Paths.FONT.value,
            Text.TITLE_SIZE.value
        ).render(Text.GAME_OVER_TEXT.value, 1, Colors.WHITE.value)
        game_over_x = Win.WIDTH.value//2 - game_over_text.get_width()//2
        game_over_y = int(Win.HEIGHT.value * Text.TITLE_HEIGHT.value)
        # Caption 1 info
        sub_text_1 = pygame.font.Font(
            Paths.FONT.value,
            Text.SUB_SIZE.value
        ).render(Text.SUB_ONE_TEXT.value, 1, Colors.WHITE.value)
        sub_x_1 = Win.WIDTH.value//2 - sub_text_1.get_width()//2
        sub_y_1 = int(Win.HEIGHT.value * Text.SUB_HEIGHT_ONE.value)
        # Caption 2 info
        sub_text_2 = pygame.font.Font(
            Paths.FONT.value,
            Text.SUB_SIZE.value
        ).render(Text.SUB_TWO_TEXT.value, 1, Colors.WHITE.value)
        sub_x_2 = Win.WIDTH.value//2 - sub_text_2.get_width()//2
        sub_y_2 = sub_y_1 + sub_text_1.get_height()
        # Display on screen
        self.win.blit(
            game_over_text,
            (game_over_x, game_over_y)
        )
        self.win.blit(
            sub_text_1,
            (sub_x_1, sub_y_1)
        )
        self.win.blit(
            sub_text_2,
            (sub_x_2, sub_y_2)
        )
        # Update
        self.update()

    def update_ship(self, ship: SpaceShip) -> None:
        """
        Updates the location of the ship. 
        Makes the image blink if the ship has been hit.
        """
        if not ship.delaying_hit(self.frame) or self.frame % 20 > 10:
            self.win.blit(ship.get_image(), ship.get_rect())

    def update_invader(self, invader: SpaceInvader) -> None:
        """
        Updates the location of a single invader.
        """
        invader.move(self.frame)
        self.win.blit(invader.get_image(), invader.get_rect())

    def update_frame(self, fps: int = 0, interval: int = 1) -> None:
        """
        Makes the clock tick and keeps track of the current frame.
        Default value for the fps variable is self.fps.
        """
        fps = self.fps if fps == 0 else fps
        self.clock.tick(fps)
        self.frame += interval

    def update_laser(self, laser: Laser) -> None:
        """
        Updates the laser position based on its speed.
        The function is called before new lasers are spawned so that
        the newly spawned lasers' y position is the same as the spaceship's,
        and not increased by vel.
        Also, so that the ship's surface covers that of any lasers coming out
        of it.
        """
        self.win.blit(laser.get_image(), laser.get_rect())

    def update(self) -> None:
        """
        Updates the whole screen, necessary for each frame.
        """
        pygame.display.update()

    def get_frame(self):
        return self.frame