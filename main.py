import pygame
from src.views.menuView import MenuView
from src.controllers.gameController import GameController
from src.views.multiplayerView import MultiplayerView

def main():
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Set the screen to windowed mode with current resolution
    pygame.display.set_caption("Multimedia Game")
    menu_view = MenuView(screen)
    
    running = True
    while running:
        selected_option = menu_view.show_menu()
        if selected_option == "Play":
            game_controller = GameController(screen)
            game_controller.run()
        elif selected_option == "Multiplayer":
            multiplayer_view = MultiplayerView(screen)
            multiplayer_view.show_multiplayer_menu()
        elif selected_option == "Quit":
            running = False

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()