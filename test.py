import pygame, time, wave

track = wave.open("assets/soundtrack.wav")

pygame.init()
pygame.mixer.quit()
pygame.mixer.init(frequency=track.getframerate())

pygame.mixer.music.load("assets/soundtrack.mp3")
pygame.mixer.music.play()

time.sleep(100)

