import pygame
from src.views.shopView import ShopView  # Import the ShopView class

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        info = pygame.display.Info()
        
        # Load background and title images
        self.background_image = pygame.image.load('assets/images/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        self.title_image = pygame.image.load('assets/images/logo.png')
        
        # Scale the logo image
        logo_width, logo_height = self.title_image.get_size()
        scale_factor = min(self.screen.get_width() // 1.1 / logo_width, self.screen.get_height() // 2 / logo_height)
        new_logo_width = int(logo_width * scale_factor)
        new_logo_height = int(logo_height * scale_factor)
        self.title_image = pygame.transform.scale(self.title_image, (new_logo_width, new_logo_height))

        # Load the shop button image and reduce its size while maintaining the aspect ratio
        self.shop_button_image = pygame.image.load('assets/images/shopSign.png')
        shop_button_width, shop_button_height = self.shop_button_image.get_size()
        shop_scale_factor = 0.5  # Adjust the scale factor as needed
        new_shop_button_width = int(shop_button_width * shop_scale_factor)
        new_shop_button_height = int(shop_button_height * shop_scale_factor)
        self.shop_button_image = pygame.transform.scale(self.shop_button_image, (new_shop_button_width, new_shop_button_height))

        # Define the help button
        self.help_button_rect = pygame.Rect(0, 0, 150, 50)  # Size of the help button
        self.help_active = False  # Control if help is active

        # Load the pixel font
        self.font = pygame.font.Font('assets/fonts/pixel.ttf', 36)
        self.help_font = pygame.font.Font('assets/fonts/pixel.ttf', 28)
        self.menu_font = pygame.font.Font('assets/fonts/pixel.ttf', 74)

    def draw_rounded_rect(self, surface, color, rect, corner_radius):
        """Draw a rectangle with rounded corners."""
        if corner_radius > 0:
            pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
        else:
            pygame.draw.rect(surface, color, rect)

    def show_menu(self):
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        
        # Define menu options with more separation
        play_text = self.menu_font.render("Play", True, (0, 0, 0))
        play_rect = play_text.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 100))
        shop_rect = self.shop_button_image.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 100))
        quit_text = self.menu_font.render("Quit", True, (0, 0, 0))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        
        # Smaller font size for the "Help" text on the button
        help_text = self.help_font.render("Help", True, (255, 255, 255))
        self.help_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 200)
        
        # List of menu options to navigate
        options = [play_rect, shop_rect, self.help_button_rect, quit_rect]
        selected_option = 0
        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Play
                            waiting = False
                        elif selected_option == 1:  # Shop
                            shop_view = ShopView(self.screen)
                            shop_view.run()
                        elif selected_option == 2:  # Help
                            self.help_active = not self.help_active  # Toggle help
                        elif selected_option == 3:  # Quit
                            pygame.quit()
                            exit()

            # Draw the background and logo
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.title_image, (WIDTH // 2 - self.title_image.get_width() // 2, HEIGHT // 6))

            # Draw menu buttons
            play_button_color = (200, 200, 200) if selected_option == 0 else (150, 150, 150)
            shop_button_color = (200, 200, 200) if selected_option == 1 else (150, 150, 150)
            help_button_color = (200, 200, 200) if selected_option == 2 else (150, 150, 150)
            quit_button_color = (200, 200, 200) if selected_option == 3 else (150, 150, 150)

            # Draw the buttons with rounded borders
            self.draw_rounded_rect(self.screen, play_button_color, play_rect.inflate(50, 10), 10)
            self.draw_rounded_rect(self.screen, help_button_color, self.help_button_rect, 5)
            self.draw_rounded_rect(self.screen, quit_button_color, quit_rect.inflate(50, 10), 10)

            # Render option texts
            play_text = self.menu_font.render("Play", True, (255, 0, 0) if selected_option == 0 else (0, 0, 0))
            quit_text = self.menu_font.render("Quit", True, (255, 0, 0) if selected_option == 3 else (0, 0, 0))

            # Draw option texts
            self.screen.blit(play_text, play_rect)
            self.screen.blit(quit_text, quit_rect)
            # Draw the shop button image with a background for selection
            if selected_option == 1:
                pygame.draw.rect(self.screen, shop_button_color, shop_rect.inflate(20, 20), border_radius=10)
            self.screen.blit(self.shop_button_image, shop_rect)
            # Place the "Help" text centered within the larger button
            self.screen.blit(help_text, (self.help_button_rect.x + (self.help_button_rect.width - help_text.get_width()) // 2,
                                         self.help_button_rect.y + (self.help_button_rect.height - help_text.get_height()) // 2))

            # Show help window if active
            if self.help_active:
                help_info = [
                    "Game Controls:",
                    "- Move: W/A/S/D",
                    "- Aim: Mouse",
                    "- Shoot: Left Click",
                    "- Pause: ESC"
                ]
                help_box_rect = pygame.Rect(100, 100, 400, 200)
                self.draw_rounded_rect(self.screen, (50, 50, 50), help_box_rect, 10)
                
                for i, line in enumerate(help_info):
                    line_surface = self.help_font.render(line, True, (255, 255, 255))
                    self.screen.blit(line_surface, (help_box_rect.x + 10, help_box_rect.y + 10 + i * 30))

            pygame.display.update()