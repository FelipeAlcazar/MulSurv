import pygame

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load('assets/images/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        
        # Cargar la imagen del logo sin escalar
        self.title_image = pygame.image.load('assets/images/logo.png')
        
        # Obtener las dimensiones originales del logo
        logo_width, logo_height = self.title_image.get_size()
        
        # Calcular la nueva escala manteniendo la relación de aspecto
        scale_factor = min(self.screen.get_width() // 1.1 / logo_width, self.screen.get_height() // 2 / logo_height)
        new_logo_width = int(logo_width * scale_factor)
        new_logo_height = int(logo_height * scale_factor)
        
        # Escalar la imagen del logo
        self.title_image = pygame.transform.scale(self.title_image, (new_logo_width, new_logo_height))

    def draw_rounded_rect(self, surface, color, rect, corner_radius):
        """ Draw a rectangle with rounded corners. """
        if corner_radius > 0:
            pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
        else:
            pygame.draw.rect(surface, color, rect)

    def show_menu(self):
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        menu_font = pygame.font.Font(None, 74)
        play_text = menu_font.render("Play", True, (0, 0, 0))
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Bajar un poco más los botones
        quit_text = menu_font.render("Quit", True, (0, 0, 0))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 280))  # Bajar un poco más los botones y más separados

        options = [play_rect, quit_rect]
        selected_option = 0

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            waiting = False
                        elif selected_option == 1:
                            pygame.quit()
                            exit()

            self.screen.fill((255, 255, 255))  # Fondo blanco
            self.screen.blit(self.background_image, (0, 0))  # Dibujar la imagen de fondo
            self.screen.blit(self.title_image, (WIDTH // 2 - self.title_image.get_width() // 2, HEIGHT // 6))  # Bajar la imagen del título

            # Dibujar botones con fondo de color y bordes redondeados
            play_button_color = (200, 200, 200) if selected_option == 0 else (150, 150, 150)
            quit_button_color = (200, 200, 200) if selected_option == 1 else (150, 150, 150)

            self.draw_rounded_rect(self.screen, play_button_color, play_rect.inflate(50, 10), 10)  # Botón más pequeño
            self.draw_rounded_rect(self.screen, quit_button_color, quit_rect.inflate(50, 10), 10)  # Botón más pequeño

            # Renderizar el texto de las opciones
            play_text = menu_font.render("Play", True, (255, 0, 0) if selected_option == 0 else (0, 0, 0))
            quit_text = menu_font.render("Quit", True, (255, 0, 0) if selected_option == 1 else (0, 0, 0))

            self.screen.blit(play_text, play_rect)
            self.screen.blit(quit_text, quit_rect)
            pygame.display.update()