
import pygame
from .game import Game

class Menu():
    def main():
        """
        Main menu of the game.
        """


    def play_game(self):
        """
        Plays game, restarts iteratively if player chooses to restart.
        """
        status=True
        while status:
            game = Game(player=self.player, difficulty=self.difficulty)
            status = game.run()



