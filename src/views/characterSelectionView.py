import pygame
from src.models.player import Player
from src.utils.data_manager import load_data, save_data
import os

class CharacterSelectionView:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Base path for assets
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")

        # Load data
        self.data = load_data()
        self.coins = self.data.get("coins", 0)
        self.unlocked_characters = self.data.get("unlocked_characters", [])

        # Load images
        self.coin_image = pygame.image.load(os.path.join(assets_path, "images", "coin.png")).convert_alpha()
        self.locked_image = pygame.image.load(os.path.join(assets_path, "images", "lock.png")).convert_alpha()

        # Colors
        self.text_color = (255, 255, 255)
        self.highlight_color = (255, 215, 0)
        self.box_color = (50, 50, 50, 200)
        self.border_color = (200, 200, 200)
        self.back_button_color = (200, 0, 0)

        # Character data
        self.characters = list(Player.predefined_characters.keys())
        self.selected_index = 0
        self.characters_data = Player.predefined_characters

        # Background
        self.background_image = pygame.image.load(os.path.join(assets_path, "images", "background.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

        # Fonts (adaptativos al tamaño de la pantalla)
        self.title_font = pygame.font.Font(os.path.join(assets_path, "fonts", "pixel.ttf"), int(self.screen.get_width() * 0.05))
        self.name_font = pygame.font.Font(os.path.join(assets_path, "fonts", "pixel.ttf"), int(self.screen.get_width() * 0.025))
        self.stats_font = pygame.font.Font(os.path.join(assets_path, "fonts", "pixel.ttf"), int(self.screen.get_width() * 0.02))
        self.unlock_font = pygame.font.Font(os.path.join(assets_path, "fonts", "pixel.ttf"), int(self.screen.get_width() * 0.02))
        self.button_font = pygame.font.Font(os.path.join(assets_path, "fonts", "pixel.ttf"), int(self.screen.get_width() * 0.03))
        self.coin_font = pygame.font.Font(os.path.join(assets_path, "fonts", "pixel.ttf"), int(self.screen.get_width() * 0.03))

    def draw_coins(self):
        """Dibuja la cantidad de monedas actuales."""
        coin_size = int(self.screen.get_width() * 0.04)  # Tamaño proporcional al ancho
        self.coin_image = pygame.transform.scale(self.coin_image, (coin_size, coin_size))
        self.screen.blit(self.coin_image, (10, 10))
        coins_text = self.coin_font.render(str(self.coins), True, self.text_color)
        self.screen.blit(coins_text, (10 + coin_size + 10, 10 + coin_size // 4))

    def draw(self):
        """Dibuja la pantalla de selección de personaje."""
        self.screen.blit(self.background_image, (0, 0))

        # Título
        title_text = self.title_font.render("Select Your Character", True, self.text_color)
        title_x = (self.screen.get_width() - title_text.get_width()) // 2
        self.screen.blit(title_text, (title_x, int(self.screen.get_height() * 0.1)))

        # Parámetros responsivos para las cajas
        box_width = int(self.screen.get_width() * 0.2)
        box_height = int(self.screen.get_height() * 0.4)
        spacing = int(self.screen.get_width() * 0.02)
        start_x = (self.screen.get_width() - (len(self.characters) * box_width + (len(self.characters) - 1) * spacing)) // 2
        start_y = int(self.screen.get_height() * 0.3)

        for i, character_name in enumerate(self.characters):
            character_data = self.characters_data[character_name]
            box_x = start_x + i * (box_width + spacing)
            box_y = start_y

            # Caja del personaje
            box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            surface.fill(self.box_color)
            self.screen.blit(surface, (box_x, box_y))

            # Selección destacada
            if i == self.selected_index:
                pygame.draw.rect(self.screen, self.highlight_color, box_rect, 4)
            else:
                pygame.draw.rect(self.screen, self.border_color, box_rect, 2)

            # Imagen del personaje
            image_path = character_data["image_path"]
            if os.path.exists(image_path):
                character_image = pygame.image.load(image_path).convert_alpha()
                char_width = box_width - 20
                char_height = int(box_height * 0.5)
                character_image = pygame.transform.scale(character_image, (char_width, char_height))

                if character_name not in self.unlocked_characters:
                    # Imagen en escala de grises si está bloqueado
                    character_image = character_image.copy()
                    arr = pygame.surfarray.pixels3d(character_image)
                    avg = arr.mean(axis=2, keepdims=True)
                    arr[:] = avg
                    del arr

                image_x = box_x + (box_width - char_width) // 2
                self.screen.blit(character_image, (image_x, box_y + 10))

            # Nombre del personaje
            name_text = self.name_font.render(character_name, True, self.text_color)
            name_x = box_x + (box_width - name_text.get_width()) // 2
            self.screen.blit(name_text, (name_x, box_y + char_height + 20))

            # Estadísticas o bloqueo
            stats_y = box_y + char_height + 60
            if character_name in self.unlocked_characters:
                speed_text = "Speed: Very Fast" if character_data["speed"] > 8 else "Speed: Fast" if character_data["speed"] > 6 else "Speed: Slow"
                size_text = "Size: Large" if character_data["size"] > 50 else "Size: Small"
                stats = [speed_text, size_text]
                for stat in stats:
                    stat_text = self.stats_font.render(stat, True, self.text_color)
                    self.screen.blit(stat_text, (box_x + (box_width - stat_text.get_width()) // 2, stats_y))
                    stats_y += 30
            else:
                cost = character_data.get("cost", 50)
                unlock_text = f"Locked - {cost} Coins"
                unlock_text_render = self.unlock_font.render(unlock_text, True, (255, 0, 0))
                self.screen.blit(unlock_text_render, (box_x + (box_width - unlock_text_render.get_width()) // 2, stats_y))

                lock_size = int(box_width * 0.3)
                lock_image = pygame.transform.scale(self.locked_image, (lock_size, lock_size))
                lock_x = box_x + (box_width - lock_size) // 2
                lock_y = box_y + 10 + (char_height - lock_size) // 2
                self.screen.blit(lock_image, (lock_x, lock_y))

        # Botón de regreso
        button_width = int(self.screen.get_width() * 0.2)
        button_height = int(self.screen.get_height() * 0.08)
        button_x = (self.screen.get_width() - button_width) // 2
        button_y = int(self.screen.get_height() * 0.85)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        if self.selected_index == len(self.characters):  # Destacar si se selecciona el botón
            pygame.draw.rect(self.screen, (255, 0, 0), button_rect.inflate(10, 10), border_radius=10)
        pygame.draw.rect(self.screen, self.back_button_color, button_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.border_color, button_rect, 2, border_radius=10)

        button_text = self.button_font.render("Back", True, self.text_color)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)

        self.draw_coins()
        pygame.display.flip()

    def run(self):
        """Ejecuta la pantalla de selección de personajes."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % (len(self.characters) + 1)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % (len(self.characters) + 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = len(self.characters)  # Ir al botón Back
                    elif event.key == pygame.K_UP:
                        if self.selected_index == len(self.characters):
                            self.selected_index = 0  # Subir desde Back
                    elif event.key == pygame.K_RETURN:
                        if self.selected_index == len(self.characters):  # Botón Back
                            return None
                        else:
                            selected_character = self.characters[self.selected_index]
                            if selected_character in self.unlocked_characters:
                                return selected_character
                            else:
                                return "store"
                    elif event.key == pygame.K_ESCAPE:
                        return None

            self.draw()
            self.clock.tick(30)