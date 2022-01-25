"""
DOCSTRING

This file includes all objects handling visual changes.

The Window object handles all surfaces on display. It also handles the clock, which 
dictates the game's pace, and includes an attribute tracking the frame number, which is
important for many methods. The background, hearts, and earth icons are also attributes.
"""
from curses.ascii import SUB
import pygame_textinput as pgti
import pygame
import os

from .base import Base
from .laser import Laser
from .space_ship import SpaceShip
from .constants import Paths, Colors, Titles, Win, Health, Score, Buttons, Table
from .space_invader import SpaceInvader


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
        self.background = pygame.image.load(background)
        self.font  = font
        self.clock = pygame.time.Clock()
        self.frame = 0 # The current nth frame.
        self.title_font = pygame.font.Font(
            Paths.FONT.value,
            Titles.TITLE_SIZE.value
        )
        self.sub_font = pygame.font.Font(
            Paths.FONT.value,
            Titles.SUB_SIZE.value
        )
        self.button_font = pygame.font.Font(
            Paths.FONT.value,
            Buttons.SIZE.value
        )
        self.return_font = pygame.font.Font(
            Paths.FONT.value,
            Buttons.SIZE.value * 3 // 4
        )
        self.cell_font = pygame.font.Font(
            Paths.FONT.value,
            Table.SIZE.value
        )
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

# Menu methods

    def blit_background(self):
        # Display Background
        self.win.blit(
            self.background,
            (0,0)
        )
    
    def blit_title(self, text="Space Invaders"):
        # Display Title
        title = self.title_font.render(
            text, 
            1, 
            Colors.WHITE.value
        )
        title_x = Win.WIDTH.value//2 - title.get_width()//2
        title_y = Titles.TITLE_HEIGHT.value 
        self.win.blit(
            title,
            (title_x, title_y)
        )
    
    def blit_sub(self, text: str, height:int=-1):
        if height == -1:
            height = Titles.SUB_HEIGHT.value

        sub = self.sub_font.render(text, 1, Colors.WHITE.value)
        sub_x = Win.WIDTH.value//2 - sub.get_width()//2
        sub_y = height 
        self.win.blit(
            sub,
            (sub_x, sub_y)
        )

    def blit_button(self, text: str, height: int) -> pygame.Rect:
        # Display Button
        button = self.button_font.render(
            text, 
            1, 
            Colors.WHITE.value
        )
        button_x = Win.WIDTH.value//2 - button.get_width()//2
        button_y = height
        self.win.blit(
            button,
            (button_x, button_y)
        )
        # Extract rectangle so you can return it
        button_rect = button.get_rect().move(button_x, button_y)

        return button_rect

    def blit_return(self, text="Back", left=True) -> pygame.Rect:
        #Display Return Button
        ret = self.return_font.render(
            text,
            1,
            Colors.WHITE.value
        )
        ret_x = Buttons.RET_X.value if left else\
             Win.WIDTH.value - Buttons.RET_X.value - ret.get_rect().width
        ret_y = Buttons.RET_Y.value 
        self.win.blit(
            ret,
            (ret_x, ret_y)
        )
        # Update position of return rectangle
        ret_rect = ret.get_rect().move(ret_x, ret_y)  

        return ret_rect

    def blit_cell(self, text: str, x: int, y: int) -> None:
        # Displays table cell
        cell = self.return_font.render(
            str(text),
            1,
            Colors.WHITE.value
        )
        self.win.blit(
            cell,
            (x, y)
        )

    def welcome_back(self, name: str) -> None:
        """
        Displays screen welcoming a player who has played before.
        """
        self.blit_background()
        self.blit_title(text=f"Welcome Back, {name}!")

    def welcome_new(self, name: str) -> None:
        """
        Displays screen welcoming a player who has played before.
        """
        self.blit_background()
        self.blit_title(text=f"Welcome {name}")

        # Display instructions
        self.blit_sub(text="Press the spacebar to shoot", height=400)
        self.blit_sub(text="and the arrow keys to move", height=440)
    
    def get_input(self) -> pgti.TextInputVisualizer:
        input = pgti.TextInputVisualizer(
            font_object=self.button_font,
            font_color=Colors.WHITE.value,
            cursor_blink_interval=700,
            cursor_color=Colors.WHITE.value
        )
        return input

    def manage_input(self, input: pgti.TextInputVisualizer, events) -> None:
        input.update(events)
        input_x = (Win.WIDTH.value - input.surface.get_rect().width) // 2
        input_y = Buttons.FIRST_Y.value + Buttons.SPACING.value
        self.win.blit(input.surface,(input_x, input_y))

# Game methods

    def scroll(self) -> None:
        """
        Adds background image and infinite scrolling.
        """
        def rect_desc(num: int) -> tuple:
            # The background is displayed lower by num, higher if num<0
            return (self.background.get_rect().left, self.background.get_rect().top-num)

        background_height = self.background.get_rect().height
        frame = self.frame % background_height
        # Represent the background shifted down according to frame
        self.win.blit(
            self.background, 
            rect_desc(frame)
        )
        # Blit a second background underneath the current one if the
        # current one's lower border has shifted above the visible screen
        if frame > background_height-self.height:
            offset = frame - background_height
            self.win.blit(
                self.background,
                rect_desc(offset)
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

    def get_win(self):
        return self.win