import pygame
from src.models.player import Player
from src.utils.data_manager import load_data, save_data
import os

class ShopView:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Base path for assets
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")

        # Cargar datos de monedas y personajes desbloqueados
        self.data = load_data()
        self.coins = self.data.get("coins", 0)
        self.unlocked_characters = self.data.get("unlocked_characters", [])

        # Cargar imagen de la moneda y aumentar su tamaño
        self.coin_image = pygame.image.load(os.path.join(assets_path, "images", "coin.png")).convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (48, 48))
        
        # Cargar imagen de candado
        self.locked_image = pygame.image.load(os.path.join(assets_path, "images", "lock.png")).convert_alpha()
        self.locked_image = pygame.transform.scale(self.locked_image, (32, 32))

        # Colores
        self.background_color = (30, 30, 30)  # Fondo oscuro
        self.box_color = (50, 50, 50, 220)     # Color del recuadro
        self.border_color = (200, 200, 0)      # Color del borde (amarillo)
        self.text_color = (255, 255, 255)      # Color del texto
        self.highlight_color = (255, 255, 0)   # Color para el personaje seleccionado
        self.back_button_color = (200, 0, 0)    # Color del botón "Volver" (rojo)
        
        # Datos de los personajes
        self.characters_data = Player.predefined_characters
        self.characters = list(self.characters_data.keys())
        self.selected_index = 0
        self.selected_button = 1  # 1 para personajes, 0 para el botón "Back"
        
        # Button properties
        self.button_width = 200
        self.button_height = 50
        self.button_rect = pygame.Rect(
            (self.screen.get_width() - self.button_width) // 2,
            self.screen.get_height() - self.button_height - 20,
            self.button_width,
            self.button_height
        )
        
        # Load the pixel font
        self.font = pygame.font.Font(os.path.join(assets_path, 'fonts', 'pixel.ttf'), 42)
        self.title_font = pygame.font.Font(os.path.join(assets_path, 'fonts', 'pixel.ttf'), 56)
        self.name_font = pygame.font.Font(os.path.join(assets_path, 'fonts', 'pixel.ttf'), 30)
        self.unlock_font = pygame.font.Font(os.path.join(assets_path, 'fonts', 'pixel.ttf'), 30)
        self.button_font = pygame.font.Font(os.path.join(assets_path, 'fonts', 'pixel.ttf'), 34)

    def draw_coins(self):
        # Obtener el ancho de la pantalla
        screen_width = self.screen.get_width()
        
        # Calcular la posición x para que la imagen esté en la esquina superior derecha
        coin_x = screen_width - self.coin_image.get_width() - 100  # 100 píxeles de margen desde el borde derecho
        
        # Dibujar la imagen en la nueva posición
        coin_y = 10  # 10 píxeles de margen desde el borde superior
        self.screen.blit(self.coin_image, (coin_x, coin_y))
        
        # Dibujar el número de monedas al lado de la imagen
        coins_text = self.font.render(f"x {self.coins}", True, (255, 255, 255))
        
        # Asegurarse de que el texto esté alineado horizontalmente con la imagen
        text_y = coin_y + (self.coin_image.get_height() - coins_text.get_height()) // 2
        self.screen.blit(coins_text, (coin_x + self.coin_image.get_width() + 5, text_y))
        
    def draw(self):
        # Dibujar fondo
        self.screen.fill(self.background_color)

        # Título en mayúsculas
        title_text = self.title_font.render("SHOP - BUY CHARACTERS", True, self.text_color)
        title_x = self.screen.get_width() // 2 - title_text.get_width() // 2
        self.screen.blit(title_text, (title_x, 50))

        # Configuración de recuadros
        box_width = 220
        box_height = 300
        spacing = 50
        start_x = (self.screen.get_width() - ((box_width + spacing) * len(self.characters) - spacing)) // 2
        start_y = self.screen.get_height() // 3

        for i, character_name in enumerate(self.characters):
            character_data = self.characters_data[character_name]
            box_x = start_x + i * (box_width + spacing)
            box_y = start_y

            # Fondo del recuadro semitransparente
            box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            surface.fill(self.box_color)
            self.screen.blit(surface, (box_x, box_y))

            # Sombra del recuadro
            shadow_rect = box_rect.move(5, 5)
            pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=10)

            # Resaltar el recuadro seleccionado
            if i == self.selected_index and self.selected_button == 1:
                pygame.draw.rect(self.screen, self.highlight_color, box_rect, 4, border_radius=10)
                # Recuadro blanco alrededor del personaje seleccionado
                pygame.draw.rect(self.screen, (255, 255, 255), box_rect, 2, border_radius=10)
            else:
                pygame.draw.rect(self.screen, self.border_color, box_rect, 2, border_radius=10)

            # Imagen del personaje
            image_path = character_data["image_path"]
            if os.path.exists(image_path):
                character_image = pygame.image.load(image_path).convert_alpha()
                character_image = pygame.transform.scale(character_image, (box_width - 20, box_height // 2))
                if character_name not in self.unlocked_characters:
                    # Convert the image to black and white
                    character_image = character_image.copy()
                    arr = pygame.surfarray.pixels3d(character_image)
                    avg = arr.mean(axis=2, keepdims=True)
                    arr[:] = avg
                    del arr
                image_x = box_x + (box_width - character_image.get_width()) // 2
                self.screen.blit(character_image, (image_x, box_y + 10))

            # Nombre del personaje
            name_text = self.name_font.render(character_name, True, self.text_color)
            name_x = box_x + (box_width - name_text.get_width()) // 2
            self.screen.blit(name_text, (name_x, box_y + box_height // 2 + 20))

            # Costo del personaje
            cost = character_data.get("cost")
            if character_name in self.unlocked_characters:
                unlock_text = "Unlocked"
                unlock_color = (0, 255, 0)
            else:
                unlock_text = f"Buy for {cost} Coins"
                unlock_color = (255, 0, 0)

            unlock_text_render = self.unlock_font.render(unlock_text, True, unlock_color)
            self.screen.blit(unlock_text_render, (box_x + (box_width - unlock_text_render.get_width()) // 2, box_y + box_height // 2 + 60))

            if unlock_text != "Unlocked":
                # Make the lock image bigger and center it on the character image
                lock_image = pygame.transform.scale(self.locked_image, (64, 64))
                lock_x = image_x + (character_image.get_width() - lock_image.get_width()) // 2
                lock_y = box_y + 10 + (character_image.get_height() - lock_image.get_height()) // 2
                self.screen.blit(lock_image, (lock_x, lock_y))

        # Botón de "Back" en rojo
        if self.selected_button == 0:  # Si el botón "Back" está seleccionado
            pygame.draw.rect(self.screen, (255, 0, 0), self.button_rect.inflate(10, 10), border_radius=10)  # Bordes agrandados para resaltar
            pygame.draw.rect(self.screen, (255, 255, 255), self.button_rect, 2, border_radius=10)  # Borde blanco
        else:
            pygame.draw.rect(self.screen, self.back_button_color, self.button_rect, border_radius=10)  # Color rojo normal

        back_button_text = self.button_font.render("Back", True, self.text_color)
        back_button_text_rect = back_button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(back_button_text, back_button_text_rect)

        self.draw_coins()
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si se hizo clic en el botón de "Back"
            if self.button_rect.collidepoint(event.pos):
                return True  # Indica volver al menú principal
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Permitir volver con ESC
                return True  # Indica volver al menú principal
            elif event.key == pygame.K_LEFT:
                if self.selected_button == 1:  # Si estamos en la navegación de personajes
                    if len(self.characters) > 0:  # Solo navegar si hay personajes
                        self.selected_index = (self.selected_index - 1) % len(self.characters)
                else:
                    self.selected_button = 1  # Cambiar a navegación de personajes
            elif event.key == pygame.K_RIGHT:
                if self.selected_button == 1:  # Si estamos en la navegación de personajes
                    if len(self.characters) > 0:  # Solo navegar si hay personajes
                        self.selected_index = (self.selected_index + 1) % len(self.characters)
                else:
                    self.selected_button = 1  # Cambiar a navegación de personajes
            elif event.key == pygame.K_DOWN:
                self.selected_button = 0  # Seleccionar el botón "Back"
            elif event.key == pygame.K_UP:
                if self.selected_button == 0:
                    self.selected_button = 1  # Cambiar a navegación de personajes
            elif event.key == pygame.K_RETURN:
                if self.selected_button == 0:  # Si se selecciona el botón "Back"
                    return True  # Indica volver al menú principal
                else:  # Selección de personaje
                    if len(self.characters) > 0:  # Solo permitir comprar si hay personajes
                        selected_character = self.characters[self.selected_index]
                        cost = self.characters_data[selected_character].get("cost", 50)

                        if selected_character in self.unlocked_characters:
                            print(f"{selected_character} ya está desbloqueado.")
                        elif self.coins >= cost:
                            self.coins -= cost
                            self.data["coins"] = self.coins
                            self.unlocked_characters.append(selected_character)
                            self.data["unlocked_characters"] = self.unlocked_characters
                            save_data(self.data)
                            print(f"{selected_character} comprado!")
                        else:
                            print("¡No tienes suficientes monedas!")

        return False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.handle_event(event):
                    running = False  # Salir si se pulsa el botón de "Back"

            self.draw()
            self.clock.tick(30)