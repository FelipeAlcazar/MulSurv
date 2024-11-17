import pygame
from src.controllers.serverController import Server
from src.controllers.clientController import Client
from src.controllers.multiGameController import MultiPlayerGameController

class MultiplayerView:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        info = pygame.display.Info()
        
        # Load background image
        self.background_image = pygame.image.load('assets/images/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

        # Load the pixel font
        self.font = pygame.font.Font('assets/fonts/pixel.ttf', 60)

        # Define button properties
        self.button_width = 300
        self.button_height = 100
        self.button_color = (70, 70, 70)
        self.button_hover_color = (90, 90, 90)  # Slightly lighter grey for hover
        self.button_text_color = (255, 255, 255)
        self.button_font = pygame.font.Font('assets/fonts/pixel.ttf', 48)

        # Define button positions
        self.host_button_rect = pygame.Rect(
            (self.screen.get_width() - self.button_width) // 2,
            self.screen.get_height() // 2 - self.button_height - 20,
            self.button_width,
            self.button_height
        )
        self.join_button_rect = pygame.Rect(
            (self.screen.get_width() - self.button_width) // 2,
            self.screen.get_height() // 2 + 20,
            self.button_width,
            self.button_height
        )

    def draw_rounded_rect(self, surface, color, rect, radius):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def show_multiplayer_menu(self):
        menu_options = ["Host", "Join"]
        option_rects = [self.host_button_rect, self.join_button_rect]
        selected_option = 0

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if menu_options[selected_option] == "Host":
                            server = Server()
                            server.run()
                            game_controller = MultiPlayerGameController(self.screen, is_server=True)
                            game_controller.run_multiplayer_game()
                        elif menu_options[selected_option] == "Join":
                            client = Client()
                            client.run()
                            game_controller = MultiPlayerGameController(self.screen, is_server=False)
                            game_controller.run_multiplayer_game()
                        return menu_options[selected_option]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i, rect in enumerate(option_rects):
                            if rect.collidepoint(event.pos):
                                if menu_options[i] == "Host":
                                    server = Server()
                                    server.run()
                                    game_controller = MultiPlayerGameController(self.screen, is_server=True)
                                    game_controller.run_multiplayer_game()
                                elif menu_options[i] == "Join":
                                    client = Client()
                                    client.run()
                                    game_controller = MultiPlayerGameController(self.screen, is_server=False)
                                    game_controller.run_multiplayer_game()
                                return menu_options[i]

            self.screen.fill((0, 0, 0))  # Dark background
            self.screen.blit(self.background_image, (0, 0))

            # Draw menu options with rounded backgrounds
            for i, option in enumerate(menu_options):
                rect = option_rects[i]
                if rect.collidepoint(mouse_pos):
                    selected_option = i

                if selected_option == i:
                    color = (255, 255, 0)  # Yellow for selected options
                    bg_color = (50, 50, 50)  # Dark grey background for selected option
                else:
                    color = (255, 255, 255)  # White for unselected options
                    bg_color = (30, 30, 30)  # Darker grey background for unselected options

                # Draw rounded background
                self.draw_rounded_rect(self.screen, bg_color, rect, 20)

                # Draw text
                text_surface = self.button_font.render(option, True, color)
                self.screen.blit(text_surface, text_surface.get_rect(center=rect.center))

            pygame.display.update()