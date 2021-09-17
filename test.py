import pygame

from window import Window
from spawner import Spawner
from space_ship import SpaceShip
from space_invader import SpaceInvader
from enums import Win, Paths, Ship, Invader, Spawning

screen = Window(
    width=Win.WIDTH.value,
    height=Win.HEIGHT.value,
    caption="Space Invaders!",
    path=Paths.BACKGROUND.value
)
space_ship = SpaceShip(
    vel=Ship.VEL.value,
    lives=Ship.LIVES.value,
    init_x=Ship.INITX.value,
    init_y=Ship.INITY.value,
    width=Ship.WIDTH.value,
    height=Ship.HEIGHT.value,
    path=Paths.SHIP.value
)
spawner = Spawner(
    initial = Spawning.INIT.value,
    later = Spawning.LATER.value
)

def main():
    # Play music
    pygame.mixer.init()
    pygame.mixer.music.load(Paths.MUSIC.value)
    pygame.mixer.music.play(-1)
    # Start clock, init other variables
    clock = pygame.time.Clock()
    frame, score = 0, 0
    run = True
    # Spawn the invaders!
    invaders = spawner.init_spawn()
    # Run the game
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        clock.tick(Win.FPS.value) # Loops at 60 fps
        frame += 1
        # Spawn new invaders
        if frame%Spawning.INTERVAL.value == 0:
            invaders.extend(spawner.later_spawn())
        # Register pressed keys (left or right)
        keys_pressed = pygame.key.get_pressed()
        # Update screen
        screen.scroll(frame)
        screen.update_ship(space_ship, keys_pressed)
        screen.update_invaders(frame, space_ship, invaders)
        screen.update()
    # Quit if loop is broken
    pygame.quit() 

if __name__ == "__main__":
    main()