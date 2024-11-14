import pygame
from src.views.shopView import ShopView  # Import the ShopView class

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        info = pygame.display.Info()
        
        # Load background image
        self.background_image = pygame.image.load('assets/images/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        
        # Load the shop button image and reduce its size while maintaining the aspect ratio
        self.shop_button_image = pygame.image.load('assets/images/shopSign.png')
        shop_button_width, shop_button_height = self.shop_button_image.get_size()
        shop_scale_factor = 0.5  # Adjust the scale factor as needed
        new_shop_button_width = int(shop_button_width * shop_scale_factor)
        new_shop_button_height = int(shop_button_height * shop_scale_factor)
        self.shop_button_image = pygame.transform.scale(self.shop_button_image, (new_shop_button_width, new_shop_button_height))

        # Load the logo image
        self.logo_image = pygame.image.load('assets/images/logo.png')
        logo_width, logo_height = self.logo_image.get_size()
        logo_scale_factor = 0.5  # Adjust the scale factor as needed
        new_logo_width = int(logo_width * logo_scale_factor)
        new_logo_height = int(logo_height * logo_scale_factor)
        self.logo_image = pygame.transform.scale(self.logo_image, (new_logo_width, new_logo_height))

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

    def draw_faded_rect(self, surface, rect, color):
        """Draw a rectangle with a faded end."""
        for i in range(rect.width):
            alpha = 255 - (255 * i // rect.width)
            faded_color = (color[0], color[1], color[2], alpha)
            pygame.draw.line(surface, faded_color, (rect.x + i, rect.y), (rect.x + i, rect.y + rect.height))

    def show_menu(self):
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h

        # Define menu options
        menu_options = ["Play", "Shop", "Help", "Quit"]
        option_rects = []
        max_width = 0

        # Calculate scaling factor based on screen height
        scale_factor = HEIGHT / 1080  # Assuming 1080p as the base resolution

        for i, option in enumerate(menu_options):
            text_surface = self.menu_font.render(option, True, (255, 255, 255))  # Base color is white
            rect = text_surface.get_rect(center=(WIDTH // 2, int(HEIGHT // 2 + 100 * scale_factor + i * 120 * scale_factor)))  # Adjusted positions
            option_rects.append(rect)
            if rect.width > max_width:
                max_width = rect.width

        # Define the size of the background rectangles
        bg_width = int((max_width + 300) * scale_factor)  # Adjusted width
        bg_height = int((option_rects[0].height + 40) * scale_factor)  # Adjusted height

        selected_option = 0
        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
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

            # Draw the background
            self.screen.fill((0, 0, 0))  # Dark background
            self.screen.blit(self.background_image, (0, 0))

            # Draw the logo at the top center
            logo_rect = self.logo_image.get_rect(center=(WIDTH // 2, int(HEIGHT // 4 * scale_factor)))
            self.screen.blit(self.logo_image, logo_rect)

            # Draw menu options with rounded backgrounds
            for i, option in enumerate(menu_options):
                rect = option_rects[i]
                if selected_option == i:
                    if option == "Quit":
                        color = (255, 0, 0)  # Red for selected Quit option
                    else:
                        color = (255, 255, 0)  # Yellow for other selected options
                    bg_color = (50, 50, 50)  # Dark grey background for selected option
                else:
                    color = (255, 255, 255)  # White for unselected options
                    bg_color = (30, 30, 30)  # Darker grey background for unselected options

                # Draw rounded background
                bg_rect = pygame.Rect(WIDTH // 2 - bg_width // 2, rect.y - int(20 * scale_factor), bg_width, bg_height)
                self.draw_rounded_rect(self.screen, bg_color, bg_rect, int(20 * scale_factor))

                # Draw text
                text_surface = self.menu_font.render(option, True, color)
                self.screen.blit(text_surface, rect)

            # Show help window if active
            if self.help_active:
                help_info = [
                    "Game Controls:",
                    "- Move: W/A/S/D",
                    "- Aim: Mouse",
                    "- Shoot: Auto",
                    "- Pause: ESC"
                ]
                help_box_rect = pygame.Rect(100, 100, int(400 * scale_factor), int(200 * scale_factor))
                self.draw_rounded_rect(self.screen, (50, 50, 50), help_box_rect, int(10 * scale_factor))

                for i, line in enumerate(help_info):
                    line_surface = self.help_font.render(line, True, (255, 255, 255))
                    self.screen.blit(line_surface, (help_box_rect.x + 10, help_box_rect.y + 10 + i * int(30 * scale_factor)))

            pygame.display.update()