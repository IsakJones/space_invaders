"""
DOCSTRING

The Sound class handles all sound in the game, including the menu song,
the game song, the game over sound, and the laser sound. It also fixes a bug
where the pygame mixer played sound sped up by leveraging the wave library
and specifying a frequency.

"""

import pygame
import wave

class Sound():
    def __init__(self, menu_soundtrack, soundtrack, game_over, laser) -> None:
        self.soundtrack = soundtrack
        self.menu = menu_soundtrack
        self.game_over = game_over

        # To avoid frequency bug, restart mixer
        pygame.mixer.quit() 

        # Change system frequency according to any .wav file
        freq = wave.open(self.soundtrack).getframerate()
        pygame.mixer.init(frequency=freq)

        self.laser = pygame.mixer.Sound(laser)
        self.laser.set_volume(0.2) # Too loud otherwise


    def play_soundtrack(self):
        """
        Plays soundtrack. Default is "soundtrack.mp3".
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.soundtrack)
        pygame.mixer.music.play(-1) # -1 is infinite loop

    def play_menu(self):
        """
        Plays soundtrack. Default is "soundtrack.mp3".
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.menu)
        pygame.mixer.music.play(-1) # -1 is infinite loop

    def play_game_over(self):
        """
        Plays game over theme. Default is "game_over.mp3".
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.game_over)
        pygame.mixer.music.play(1) 

    def play_laser(self):
        """
        Plays laser sound. 
        """
        self.laser.play() 