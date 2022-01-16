""" 
DOCSTRING
    
This file contains the main function, which runs the game and handles the restart.
The restart is iterative as opposed to recursive (i.e. if the player chooses to 
restart, main is not called within main) to avoid a stack overflow upon successive
restarts.
""" 
from src.game import Game

def main(status=True):
    """
    Plays game, restarts iteratively if player chooses to restart.
    """
    while status:
        game = Game()
        status = game.run()

if __name__ == "__main__":
    main()