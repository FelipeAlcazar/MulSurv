import pygame
from src.controllers.gameController import GameController

def main():
    pygame.init()
    game_controller = GameController()
    game_controller.run()

if __name__ == "__main__":
    main()
    