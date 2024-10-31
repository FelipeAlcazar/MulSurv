import pygame

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        info = pygame.display.Info()
        
        # Cargar imágenes de fondo y título
        self.background_image = pygame.image.load('assets/images/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        self.title_image = pygame.image.load('assets/images/logo.png')
        
        # Escalar la imagen del logo
        logo_width, logo_height = self.title_image.get_size()
        scale_factor = min(self.screen.get_width() // 1.1 / logo_width, self.screen.get_height() // 2 / logo_height)
        new_logo_width = int(logo_width * scale_factor)
        new_logo_height = int(logo_height * scale_factor)
        self.title_image = pygame.transform.scale(self.title_image, (new_logo_width, new_logo_height))

        # Definir el botón de ayuda en la esquina superior derecha (más grande)
        self.help_button_rect = pygame.Rect(self.screen.get_width() - 110, 10, 100, 50)  # Botón más grande
        self.help_active = False  # Controlar si la ayuda está activa

    def draw_rounded_rect(self, surface, color, rect, corner_radius):
        """Dibuja un rectángulo con bordes redondeados."""
        if corner_radius > 0:
            pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
        else:
            pygame.draw.rect(surface, color, rect)

    def show_menu(self):
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        menu_font = pygame.font.Font(None, 74)
        
        # Definir las opciones del menú
        play_text = menu_font.render("Play", True, (0, 0, 0))
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
        quit_text = menu_font.render("Quit", True, (0, 0, 0))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 280))
        
        # Reducir el tamaño de fuente para el texto "Help" en el botón
        help_font = pygame.font.Font(None, 28)  # Fuente más pequeña para "Help"
        help_text = help_font.render("Help", True, (255, 255, 255))
        
        # Lista de opciones en el menú para navegar
        options = [play_rect, quit_rect, self.help_button_rect]
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
                        elif selected_option == 1:  # Quit
                            pygame.quit()
                            exit()
                        elif selected_option == 2:  # Help
                            self.help_active = not self.help_active  # Alterna la ayuda

            # Dibujar el fondo y el logo
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.title_image, (WIDTH // 2 - self.title_image.get_width() // 2, HEIGHT // 6))

            # Dibujar botones de menú
            play_button_color = (200, 200, 200) if selected_option == 0 else (150, 150, 150)
            quit_button_color = (200, 200, 200) if selected_option == 1 else (150, 150, 150)
            help_button_color = (200, 200, 200) if selected_option == 2 else (150, 150, 150)

            # Dibujar los botones con el borde redondeado
            self.draw_rounded_rect(self.screen, play_button_color, play_rect.inflate(50, 10), 10)
            self.draw_rounded_rect(self.screen, quit_button_color, quit_rect.inflate(50, 10), 10)
            self.draw_rounded_rect(self.screen, help_button_color, self.help_button_rect, 5)

            # Renderizar texto de opciones
            play_text = menu_font.render("Play", True, (255, 0, 0) if selected_option == 0 else (0, 0, 0))
            quit_text = menu_font.render("Quit", True, (255, 0, 0) if selected_option == 1 else (0, 0, 0))

            # Dibujar texto de las opciones
            self.screen.blit(play_text, play_rect)
            self.screen.blit(quit_text, quit_rect)
            # Colocar el texto "Help" centrado dentro del botón más grande
            self.screen.blit(help_text, (self.help_button_rect.x + (self.help_button_rect.width - help_text.get_width()) // 2,
                                         self.help_button_rect.y + (self.help_button_rect.height - help_text.get_height()) // 2))

            # Mostrar ventana de ayuda si está activa
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
                
                help_font = pygame.font.Font(None, 30)
                for i, line in enumerate(help_info):
                    line_surface = help_font.render(line, True, (255, 255, 255))
                    self.screen.blit(line_surface, (help_box_rect.x + 10, help_box_rect.y + 10 + i * 30))

            pygame.display.update()

