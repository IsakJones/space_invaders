"""
DOCSTRING

The menu object handles all menus in the game, including the main menu, the play menu
that handles username input, the game over menu, and the stats menu, which allows the
player to view two tables. Every method corresponds to a different menu. The Menu object
makes extensive use of the Window object to update the display.

All attributes' initializing variables are pulled from their respective 
"enum" in the constants file. Changing initializing variables for 
testing should be done in the constants file.
"""

import pygame
import time

from .game import Game
from .sound import Sound
from .window import Window
from .db.database import DB
from .constants import Paths, Win, Buttons, Table

class Menu():
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.sound = Sound(
            menu_soundtrack=Paths.MENU_SOUNDTRACK.value,
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
        # Initialize database and establish connection
        self.db = DB()
        self.db.start()

    def start(self) -> None:
        """
        Main menu of the game. The player can play, see stats, or quit.
        """
        self.sound.play_menu()

        while True:
            # Blit the background and title
            self.screen.blit_background()
            self.screen.blit_title()
            # Blit play, stats, and quit buttons
            play = self.screen.blit_button(
                "Play",
                Buttons.FIRST_Y.value
            )
            stats = self.screen.blit_button(
                "Stats",
                Buttons.FIRST_Y.value + Buttons.SPACING.value
            )
            quit = self.screen.blit_button(
                "Quit",
                Buttons.FIRST_Y.value + Buttons.SPACING.value * 2
            )

            # Iterate through events to detect clicks
            for event in pygame.event.get():
                # If there's a click, check if it clicked on a button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play.collidepoint(event.pos):
                        self._play_menu()
                    elif stats.collidepoint(event.pos):
                        self._stats()
                        break
                    elif quit.collidepoint(event.pos):
                        return

                if event.type == pygame.QUIT:
                    return 
            
            # Update the screen
            self.screen.update()

    def _stats(self) -> None:
        """
        Gives choice of player stats or game stats.
        """
        while True:
            # Blit the background and title
            self.screen.blit_background()
            self.screen.blit_title()
            # Blit players and games options
            players = self.screen.blit_button(
                "Players",
                Buttons.FIRST_Y.value
            )
            games = self.screen.blit_button(
                "Games",
                Buttons.FIRST_Y.value + Buttons.SPACING.value
            )
            # Blit return option
            ret = self.screen.blit_return()
            self.screen.update()
            # Iterate through events to detect clicks
            for event in pygame.event.get():
                # If there's a click, check if it clicked on a button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if players.collidepoint(event.pos):
                        columns = ["Name", "High Score"]
                        player_list = self.db.get_players()
                        self._table(title="Players", columns=columns, data=player_list)
                    elif games.collidepoint(event.pos):
                        columns = ["Player", "Score", "Date"]
                        game_list = self.db.get_games()
                        self._table(title="Games", columns=columns, data=game_list)
                    elif ret.collidepoint(event.pos):
                        return 

                if event.type == pygame.QUIT:
                    return 

    def _table(self, title: str, columns: list, data) -> None:
        """
        Displays tabular data, either players or games.
        Data is a list of tuples, each with a database row.
        """
        # Only show 5 rows at a time, so keep track of start index
        data_index = 0
        next = None
        prev = None
        # Set x axis coordinates
        ln = len(columns)
        table_space = Win.WIDTH.value-Table.PADDING.value*2
        xs = [table_space // ln * i + Table.PADDING.value for i in range(ln)]

        while True:
            # Blit the background and title
            self.screen.blit_background()
            self.screen.blit_title(text=title)
            # Blit return and next button if there's more data
            if data_index == 0:
                ret = self.screen.blit_return()
                prev = None
            else:
                prev = self.screen.blit_return(text="Prev")
            if len(data) > data_index + 5:
                next = self.screen.blit_return(text="Next", left=False)
            # Blit column names
            for col, x in zip(columns, xs):
                self.screen.blit_cell(text=col, x=x, y=Table.FIRST_Y.value)
            # Blit rows
            for ind, row in enumerate(data[data_index:data_index+5], 1):
                y = Table.FIRST_Y.value + Table.SPACING.value * ind
                for val, x in zip(row, xs):
                    self.screen.blit_cell(text=val, x=x, y=y)

            self.screen.update()
            # Iterate through events to detect clicks
            for event in pygame.event.get():
                # If there's a click, check if it clicked on a button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if prev and prev.collidepoint(event.pos):
                        data_index -= 5
                    elif next and next.collidepoint(event.pos):
                        data_index += 5
                    elif ret.collidepoint(event.pos):
                        return 

                if event.type == pygame.QUIT:
                    return 

    def _play_menu(self):
        """
        Asks for username and queries database to see if user exists.
        Once done, it calls the play method, which plays the game.
        """
        # get input object
        input = self.screen.get_input()

        while True:
            events = pygame.event.get()
            # Blit the background and title
            self.screen.blit_background()
            self.screen.blit_title()
            # Blit insert username text, no need for rect
            self.screen.blit_button(
                "Insert Player Name:",
                Buttons.FIRST_Y.value
            )
            # Blit return and enter buttons
            ret = self.screen.blit_return()
            enter = self.screen.blit_button(
                "Enter",
                Buttons.FIRST_Y.value + Buttons.SPACING.value * 2
            )
            self.screen.manage_input(input, events)

            # Iterate through events to detect clicks
            for event in events:
                if event == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ret.collidepoint(event.pos):
                        return

                # The game starts playing if the user hits enter or clicks the enter button
                clicked_enter = event.type == pygame.MOUSEBUTTONDOWN and enter.collidepoint(event.pos)
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or clicked_enter:
                    # extract the user name
                    name = input.value
                    # Continue loop if username is empty
                    if not name:
                        continue
                    # display screen accordingly
                    if self.db.player_exists(name):
                        self.screen.welcome_back(name)
                        sleep_time = 1
                    else:
                        self.screen.welcome_new(name)
                        self.db.add_player(name)
                        sleep_time = 2

                    # update screen and hold for a second 
                    self.screen.update()
                    time.sleep(sleep_time)
                    self._play_game(name)
                    
                    return
                
            self.screen.update()

    def _play_game(self, name: str) -> None:
        """
        Plays game, restarts iteratively if player chooses to restart.
        """
        # Play new games unless the player quits
        status = True
        while status:
            # Create and run a new game
            game = Game(
                sound=self.sound,
                screen=self.screen
            )
            score = game.run()
            # Update database and check if it's a high score
            is_high_score = self.db.add_game(name, score)
            # Interrupt loop if player quits in game over menu
            status = self._game_over(is_high_score)

    def _game_over(self, is_high_score: bool) -> bool:
        """
        Handles game over. Calls game over screen in window, changes music,
        and supports the iterative restart in the main file.
        Returns true if the game should restart.
        """
        # Stop music and play sound
        self.sound.play_game_over()

        # Display game over title and high score
        self.screen.blit_title(text="Game Over")
        if is_high_score:
            self.screen.blit_sub(text="New High Score!")
        

        # Display retry and quit buttons
        retry = self.screen.blit_button(
            "Retry",
            Buttons.FIRST_Y.value
        )
        quit = self.screen.blit_button(
            "Quit",
            Buttons.FIRST_Y.value + Buttons.SPACING.value
        )
        
        while True:
            # Check for r press
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry.collidepoint(event.pos):
                        return True
                    if quit.collidepoint(event.pos):
                        return False

            # Update screen
            self.screen.update()
