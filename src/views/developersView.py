import os
import pygame

class DevelopersView:
    def __init__(self, screen):
        # Inicialización de Pygame
        self.screen = screen
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()))
        pygame.display.set_caption("Developers View")

        # Base path for assets
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")

        self.background_image = pygame.image.load(os.path.join(assets_path, "images", "background.png"))
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        
        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (50, 50, 50)

        # Fuentes
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.name_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.description_font = pygame.font.SysFont("Arial", 22)

        # Datos de los desarrolladores
        self.developers = [
            {
                "name": "Javier Pardo",
                "role": "Software Engineer",
                "photo": os.path.join(assets_path, "images", "pardo.png"),
                "qr": os.path.join(assets_path, "images", "qr_javier.png"),
            },
            {
                "name": "Carlos Sánchez",
                "role": "Software Engineer",
                "photo": os.path.join(assets_path, "images", "carlos.png"),
                "qr": os.path.join(assets_path, "images", "qr_carlos.png"),
            },
            {
                "name": "Felipe Alcázar",
                "role": "Software Engineer",
                "photo": os.path.join(assets_path, "images", "felipe.jpg"),
                "qr": os.path.join(assets_path, "images", "qr_felipe.png"),
            },
        ]

        # Cargar imágenes
        self.developer_images = [
            self.load_image(dev["photo"], (100, 100)) for dev in self.developers
        ]
        
        self.qr_images = [
            self.load_image(dev["qr"], (250, 250)) for dev in self.developers
        ]

    def load_image(self, filename, size=None):
        """Carga y redimensiona una imagen."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"La imagen {filename} no se encuentra en la ruta proporcionada.")
        
        image = pygame.image.load(filename)
        if size:
            return pygame.transform.scale(image, size)
        
        return image

    def draw_circle_image(self, surface, image, center, radius):
        """Dibuja una imagen dentro de un círculo."""
        pygame.draw.circle(surface, self.WHITE, center, radius)
        mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(mask, (0, 0, 0, 255), (radius, radius), radius)
        image = pygame.transform.smoothscale(image, (radius * 2, radius * 2))
        surface.blit(image, (center[0] - radius, center[1] - radius), special_flags=pygame.BLEND_RGBA_MIN)

    def render_text_centered(self, surface, text, font, color, center):
        """Dibuja texto centrado en una posición."""
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=center)
        surface.blit(rendered_text, text_rect)

    def draw_developers(self):
        """Dibuja la sección de los desarrolladores."""
        y_offset = 250  # Desplazar más abajo la sección de desarrolladores

        for i, developer in enumerate(self.developers):
            x = self.screen.get_width() // 4 * (i + 1) - 50
            y = y_offset

            # Dibujar la foto de los desarrolladores dentro de un círculo
            self.draw_circle_image(self.screen, self.developer_images[i], (x, y), 100)

            # Aumentar la distancia entre la foto y el texto
            text_distance = 40  # Distancia entre la foto y el texto

            # Dibujar los textos con la nueva distancia
            self.render_text_centered(self.screen, developer["name"], self.name_font, self.WHITE, (x, y + 90 + text_distance))
            self.render_text_centered(self.screen, developer["role"], self.description_font, self.GRAY, (x, y + 120 + text_distance))

            # Dibujar el código QR debajo del texto
            qr_x = x -120  # Centrar QR horizontalmente
            qr_y = y + 170 + text_distance  # Posición vertical debajo del texto
            self.screen.blit(self.qr_images[i], (qr_x, qr_y))

            

    def run(self):
        """Ejecuta el bucle principal."""
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(self.BLACK)

            # Dibujar el título
            self.render_text_centered(self.screen, "Meet the Developers", self.title_font, self.WHITE, (self.screen.get_width() // 2, 50))
            self.draw_developers()

            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            pygame.display.flip()
            clock.tick(60)

        # Do not call pygame.quit() here, just return to the main menu