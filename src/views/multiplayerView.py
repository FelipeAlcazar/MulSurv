import os
import pygame
from src.controllers.multiGameController import Game
import socket

class MultiplayerView:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        info = pygame.display.Info()
        
        # Base path for assets
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")

        # Load background image
        self.background_image = pygame.image.load(os.path.join(assets_path, 'images', 'background.png'))
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

        # Load the pixel font
        self.font = pygame.font.Font(os.path.join(assets_path, 'fonts', 'pixel.ttf'), 60)

        # Define button properties
        self.button_width = 300
        self.button_height = 100
        self.button_color = (70, 70, 70)
        self.button_hover_color = (90, 90, 90)  # Slightly lighter grey for hover
        self.button_text_color = (255, 255, 255)
        self.button_font = pygame.font.Font(os.path.join(assets_path, 'fonts', 'pixel.ttf'), 48)

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

    def get_nickname(self):
        """Pantalla para capturar el nickname del usuario."""
        nickname = ""
        input_rect = pygame.Rect(
            (self.screen.get_width() - 400) // 2,
            (self.screen.get_height() - 50) // 2,
            400,
            50
        )
        color_active = (50, 50, 200)
        color_inactive = (100, 100, 100)
        color = color_active  # Cambiar para que comience activo
        active = True  # El cuadro ya está activo desde el inicio
        error_message = ""  # Variable para mensaje de error

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Activar/desactivar input según clic
                    if input_rect.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            if nickname.strip() == "":  # Si el nickname está vacío
                                error_message = "Nickname cannot be empty!"  # Mensaje de error
                            else:
                                return nickname  # Devuelve el nickname al presionar Enter
                        elif event.key == pygame.K_ESCAPE:
                            return "BACK"
                        elif event.key == pygame.K_BACKSPACE:
                            nickname = nickname[:-1]
                        else:
                            nickname += event.unicode
                    elif event.key == pygame.K_ESCAPE:
                        return "BACK"

            self.screen.fill((0, 0, 0))  # Fondo oscuro
            self.screen.blit(self.background_image, (0, 0))

            # Dibujar cuadro de texto
            pygame.draw.rect(self.screen, color, input_rect, border_radius=10)

            # Renderizar el texto dentro del cuadro
            text_surface = self.font.render(nickname, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

            # Instrucciones
            instructions = self.font.render("Enter your nickname:", True, (255, 255, 255))
            self.screen.blit(instructions, instructions.get_rect(center=(self.screen.get_width() // 2, input_rect.y - 40)))

            # Mostrar mensaje de error si el nickname está vacío
            if error_message:
                error_surface = self.font.render(error_message, True, (255, 0, 0))  # Rojo para error
                self.screen.blit(error_surface, (self.screen.get_width() // 2 - error_surface.get_width() // 2, input_rect.y + 70))

            pygame.display.update()

    def get_host_and_port(self):
        """Pantalla para capturar el host y el puerto del servidor."""
        host = ""
        port = ""
        input_rect_host = pygame.Rect((self.screen.get_width() - 400) // 2, (self.screen.get_height() - 200) // 2, 400, 50)
        input_rect_port = pygame.Rect((self.screen.get_width() - 400) // 2, (self.screen.get_height() + 100) // 2, 400, 50)
        color_active = (50, 50, 200)
        color_inactive = (100, 100, 100)
        color_host = color_active
        color_port = color_inactive
        active_host = True
        active_port = False
        error_message = ""

        local_ip = self.get_ip()  # Obtener la IP local del usuario

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect_host.collidepoint(event.pos):
                        active_host = True
                        active_port = False
                    elif input_rect_port.collidepoint(event.pos):
                        active_host = False
                        active_port = True
                    else:
                        active_host = False
                        active_port = False
                    color_host = color_active if active_host else color_inactive
                    color_port = color_active if active_port else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active_host:
                        if event.key == pygame.K_RETURN:
                            active_host = False
                            active_port = True
                            color_host = color_inactive
                            color_port = color_active
                        elif event.key == pygame.K_ESCAPE:
                            return "BACK", "BACK"
                        elif event.key == pygame.K_BACKSPACE:
                            host = host[:-1]
                        else:
                            host += event.unicode
                    elif active_port:
                        if event.key == pygame.K_RETURN:
                            if host.strip() == "" or port.strip() == "":
                                error_message = "Host and port cannot be empty!"
                            else:
                                return host, port
                        elif event.key == pygame.K_ESCAPE:
                            return "BACK", "BACK"
                        elif event.key == pygame.K_BACKSPACE:
                            port = port[:-1]
                        else:
                            port += event.unicode
                    elif event.key == pygame.K_ESCAPE:
                        return "BACK", "BACK"

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background_image, (0, 0))

            pygame.draw.rect(self.screen, color_host, input_rect_host, border_radius=10)
            pygame.draw.rect(self.screen, color_port, input_rect_port, border_radius=10)

            text_surface_host = self.font.render(host, True, (255, 255, 255))
            self.screen.blit(text_surface_host, (input_rect_host.x + 10, input_rect_host.y + 10))

            text_surface_port = self.font.render(port, True, (255, 255, 255))
            self.screen.blit(text_surface_port, (input_rect_port.x + 10, input_rect_port.y + 10))

            instructions_host = self.font.render("Enter server host:", True, (255, 255, 255))
            self.screen.blit(instructions_host, instructions_host.get_rect(center=(self.screen.get_width() // 2, input_rect_host.y - 60)))

            instructions_port = self.font.render("Enter server port:", True, (255, 255, 255))
            self.screen.blit(instructions_port, instructions_port.get_rect(center=(self.screen.get_width() // 2, input_rect_port.y - 60)))

            if error_message:
                error_surface = self.font.render(error_message, True, (255, 0, 0))
                self.screen.blit(error_surface, (self.screen.get_width() // 2 - error_surface.get_width() // 2, input_rect_port.y + 70))

            # Mostrar la IP local en la parte inferior con letras negras
            ip_text = self.font.render(f"Your IP: {local_ip}", True, (0, 0, 0))
            self.screen.blit(ip_text, (self.screen.get_width() // 2 - ip_text.get_width() // 2, self.screen.get_height() - 50))

            pygame.display.update()

    def get_ip(self):
        """Obtiene la IP local del usuario."""
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

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
                        nickname = self.get_nickname()
                        if nickname == "BACK":
                            continue
                        host, port = self.get_host_and_port()
                        if host == "BACK" and port == "BACK":
                            continue
                        if menu_options[selected_option] == "Host":
                            game_controller = Game(nickname, host, int(port))
                        elif menu_options[selected_option] == "Join":
                            game_controller = Game(nickname, host, int(port), start_server=False)
                        return menu_options[selected_option]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i, rect in enumerate(option_rects):
                            if rect.collidepoint(event.pos):
                                nickname = self.get_nickname()
                                if nickname == "BACK":
                                    continue
                                host, port = self.get_host_and_port()
                                if host == "BACK" and port == "BACK":
                                    continue
                                if menu_options[i] == "Host":
                                    game_controller = Game(nickname, host, int(port))
                                elif menu_options[i] == "Join":
                                    game_controller = Game(nickname, host, int(port), start_server=False)
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