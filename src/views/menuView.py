import pygame
from src.views.shopView import ShopView  # Import the ShopView class
from src.views.multiplayerView import MultiplayerView  # Import the MultiplayerView class

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        info = pygame.display.Info()

        # Cargar la imagen de fondo
        self.background_image = pygame.image.load('assets/images/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

        # Cargar la imagen del logo y reducir su tamaño
        self.logo_image = pygame.image.load('assets/images/logo.png')
        logo_width, logo_height = self.logo_image.get_size()
        logo_scale_factor = 0.4
        new_logo_width = int(logo_width * logo_scale_factor)
        new_logo_height = int(logo_height * logo_scale_factor)
        self.logo_image = pygame.transform.scale(self.logo_image, (new_logo_width, new_logo_height))

        # Cargar la fuente de píxeles
        self.font = pygame.font.Font('assets/fonts/pixel.ttf', 26)
        self.menu_font = pygame.font.Font('assets/fonts/pixel.ttf', 60)

        # Variables de ayuda
        self.help_active = False

    def show_menu(self):
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h

        # Definir las opciones del menú, incluyendo las esquinas
        menu_options = ["Play", "Multiplayer", "Shop", "Help", "Quit"]
        corner_options = ["Help", "Quit"]
        option_rects = []
        corner_rects = []

        # Calcular el factor de escala basado en la altura de la pantalla
        scale_factor = HEIGHT / 1080

        # Ajustar el espaciado entre botones y su tamaño
        vertical_spacing = 150
        logo_spacing = 100

        # Obtener el ancho máximo (basado en "Multiplayer")
        sample_text_surface = self.menu_font.render("Multiplayer", True, (255, 255, 255))
        max_button_width = sample_text_surface.get_width() + 40  # Añadimos margen de 20 px a cada lado

        # Botones centrales
        for i, option in enumerate(menu_options[:3]):
            text_surface = self.menu_font.render(option, True, (255, 255, 255))
            rect = text_surface.get_rect(center=(WIDTH // 2, int(HEIGHT // 2 + logo_spacing + i * vertical_spacing * scale_factor)))
            # Ajustar el ancho del rectángulo para que coincida con el ancho máximo
            rect.width = max_button_width
            option_rects.append(rect)

        # Botón de ayuda (esquina superior derecha)
        help_button_rect = pygame.Rect(WIDTH - 160, 20, 150, 50)
        corner_rects.append(help_button_rect)

        # Botón de salir (esquina superior izquierda)
        quit_button_rect = pygame.Rect(10, 20, 150, 50)
        corner_rects.append(quit_button_rect)

        # Variables de selección
        selected_option = 0
        selected_corner = None  # None: menú central, 0: esquina derecha (Help), 1: esquina izquierda (Quit)
        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if selected_corner is None:
                        # Navegación dentro del menú central
                        if event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % len(option_rects)
                        elif event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % len(option_rects)
                        elif event.key == pygame.K_RIGHT:
                            selected_corner = 0  # Seleccionar esquina derecha (Help)
                        elif event.key == pygame.K_LEFT:
                            selected_corner = 1  # Seleccionar esquina izquierda (Quit)
                    else:
                        # Navegación desde una esquina
                        if selected_corner == 0 and event.key == pygame.K_LEFT:
                            selected_corner = None  # Volver al menú central desde Help
                        elif selected_corner == 1 and event.key == pygame.K_RIGHT:
                            selected_corner = None  # Volver al menú central desde Quit
                    if event.key == pygame.K_RETURN:
                        if selected_corner == 0:  # Help
                            self.show_help_screen()  # Mostrar la pantalla de ayuda
                        elif selected_corner == 1:  # Quit
                            return "Quit"
                        elif selected_corner is None:
                            if selected_option == 0:  # Play
                                return "Play"
                            elif selected_option == 1:  # Multiplayer
                                multiplayer_view = MultiplayerView(self.screen)
                                multiplayer_view.show_multiplayer_menu()
                            elif selected_option == 2:  # Shop
                                shop_view = ShopView(self.screen)
                                shop_view.run()

            # Dibujar el fondo
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background_image, (0, 0))

            # Dibujar el logo
            logo_rect = self.logo_image.get_rect(center=(WIDTH // 2, int(HEIGHT // 4)))
            self.screen.blit(self.logo_image, logo_rect)

            # Dibujar las opciones centrales
            for i, option in enumerate(menu_options[:3]):
                rect = option_rects[i]
                if selected_corner is None and selected_option == i:
                    color = (255, 255, 0)  # Amarillo
                    bg_color = (50, 50, 50)
                else:
                    color = (255, 255, 255)  # Blanco
                    bg_color = (30, 30, 30)
                bg_rect = pygame.Rect(WIDTH // 2 - max_button_width // 2, rect.y - 10, max_button_width, rect.height + 20)
                self.draw_rounded_rect(self.screen, bg_color, bg_rect, 15)
                text_surface = self.menu_font.render(option, True, color)
                self.screen.blit(text_surface, rect)

            # Dibujar los botones en las esquinas
            for i, rect in enumerate(corner_rects):
                if selected_corner == i:
                    color = (255, 255, 0)  # Amarillo
                    bg_color = (50, 50, 50)
                else:
                    color = (255, 255, 255)  # Blanco
                    bg_color = (30, 30, 30)
                self.draw_rounded_rect(self.screen, bg_color, rect, 15)
                text_surface = self.font.render(corner_options[i], True, color)
                self.screen.blit(text_surface, rect.move(50, 10))

            pygame.display.update()

    def draw_rounded_rect(self, surface, color, rect, radius):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def show_help_screen(self):
        """Muestra una ventana con la ayuda del juego."""
        WIDTH, HEIGHT = self.screen.get_width(), self.screen.get_height()

        help_running = True
        while help_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    help_running = False  # Salir de la ventana de ayuda

            # Dibujar la ventana de ayuda
            self.screen.fill((0, 0, 0))  # Fondo negro
            help_text = [
                "CONTROLS:",
                "- Move: W/A/S/D",
                "- Attack: Mouse Left Click",
                "",
                "MODES:",
                "- Solo: Fight waves of enemies!",
                "- Multiplayer: Battle Royale mode.",
                "",
                "UPGRADES:",
                "- Unlock powerful skills and items.",
            ]
            y_offset = 100
            for line in help_text:
                text_surface = self.font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 50

            pygame.display.update()





