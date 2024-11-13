import pygame
from src.models.player import Player
from src.utils.data_manager import load_data, save_data
import os

class CharacterSelectionView:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Cargar datos de monedas y personajes desbloqueados
        self.data = load_data()
        self.coins = self.data.get("coins", 0)  # Asegurarse de que coins tenga un valor por defecto
        self.unlocked_characters = self.data.get("unlocked_characters", [])  # Inicializar como lista vacía si no existe

        # Cargar imagen de la moneda y aumentar su tamaño
        self.coin_image = pygame.image.load("assets/images/coin.png").convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (48, 48))
        
        # Cargar imagen de candado
        self.locked_image = pygame.image.load("assets/images/lock.png").convert_alpha()
        self.locked_image = pygame.transform.scale(self.locked_image, (32, 32))

        # Colores
        self.text_color = (255, 255, 255)
        self.highlight_color = (255, 215, 0)
        self.box_color = (50, 50, 50, 200)
        self.border_color = (200, 200, 200)
        self.back_button_color = (200, 0, 0)  # Color del botón "Volver" (rojo)
        
        # Datos de los personajes
        self.characters = list(Player.predefined_characters.keys())
        self.selected_index = 0
        self.characters_data = Player.predefined_characters
        
        # Fondo
        self.background_image = pygame.image.load("assets/images/background.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

        # Estado de selección
        self.unlocking = False  # Nueva variable para gestionar el estado de desbloqueo
        self.selected_character = None  # Almacena el personaje seleccionado

        # Button properties
        self.button_width = 200
        self.button_height = 50
        self.button_color = (70, 70, 70)
        self.button_text_color = (255, 255, 255)
        self.button_font = pygame.font.Font('assets/fonts/pixel.ttf', 24)
        self.button_rect = pygame.Rect(
            (self.screen.get_width() - self.button_width) // 2,
            self.screen.get_height() - self.button_height - 20,
            self.button_width,
            self.button_height
        )
        
        # Load the pixel font
        self.font = pygame.font.Font('assets/fonts/pixel.ttf', 36)
        self.title_font = pygame.font.Font('assets/fonts/pixel.ttf', 48)
        self.name_font = pygame.font.Font('assets/fonts/pixel.ttf', 24)
        self.unlock_font = pygame.font.Font('assets/fonts/pixel.ttf', 20)
        self.weapon_font = pygame.font.Font('assets/fonts/pixel.ttf', 20)
        self.stats_font = pygame.font.Font('assets/fonts/pixel.ttf', 24)

    def draw_coins(self):
        # Dibujar la imagen de la moneda
        self.screen.blit(self.coin_image, (10, 10))
        
        # Dibujar la cantidad de monedas y aumentar el tamaño del texto
        coins_text = self.font.render(str(self.coins), True, self.text_color)
        self.screen.blit(coins_text, (70, 24))

    def draw(self):
        # Dibujar fondo
        self.screen.blit(self.background_image, (0, 0))

        # Título
        title_text = self.title_font.render("Select Your Character", True, self.text_color)
        title_x = self.screen.get_width() // 2 - title_text.get_width() // 2
        self.screen.blit(title_text, (title_x, 200))  # Lower the title

        # Configuración de recuadros
        box_width = 220
        box_height = 300
        spacing = 50
        total_width = (box_width + spacing) * len(self.characters) - spacing
        start_x = (self.screen.get_width() - total_width) // 2
        start_y = (self.screen.get_height() - box_height) // 2  # Center the character boxes vertically

        for i, character_name in enumerate(self.characters):
            character_data = self.characters_data[character_name]
            box_x = start_x + i * (box_width + spacing)
            box_y = start_y

            # Fondo del recuadro semitransparente
            box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            surface.fill(self.box_color)
            self.screen.blit(surface, (box_x, box_y))

            # Resaltar el recuadro seleccionado
            if i == self.selected_index:
                pygame.draw.rect(self.screen, self.highlight_color, box_rect, 4)
            else:
                pygame.draw.rect(self.screen, self.border_color, box_rect, 2)

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

            if character_name in self.unlocked_characters:
                # Mostrar estadísticas del personaje
                stats_y = box_y + box_height // 2 + 60
                speed_text = "Speed: Very Fast" if character_data["speed"] > 8 else "Speed: Fast" if character_data["speed"] > 6 else "Speed: Slow"
                size_text = "Size: Large" if character_data["size"] > 50 else "Size: Small"
                stats = [speed_text, size_text]
                for stat in stats:
                    stat_text = self.stats_font.render(stat, True, self.text_color)
                    self.screen.blit(stat_text, (box_x + (box_width - stat_text.get_width()) // 2, stats_y))
                    stats_y += 30
            else:
                # Mostrar costo del personaje
                cost = character_data.get("cost", 50)  # Ejemplo de costo por defecto
                unlock_text = f"Locked"
                unlock_color = (255, 0, 0)
                unlock_text_render = self.unlock_font.render(unlock_text, True, unlock_color)
                self.screen.blit(unlock_text_render, (box_x + (box_width - unlock_text_render.get_width()) // 2, box_y + box_height // 2 + 60))

                # Make the lock image bigger and center it on the character image
                lock_image = pygame.transform.scale(self.locked_image, (64, 64))
                lock_x = image_x + (character_image.get_width() - lock_image.get_width()) // 2
                lock_y = box_y + 10 + (character_image.get_height() - lock_image.get_height()) // 2
                self.screen.blit(lock_image, (lock_x, lock_y))

        # Draw the back button
        if self.selected_index == len(self.characters):
            pygame.draw.rect(self.screen, (255, 0, 0), self.button_rect.inflate(10, 10), border_radius=10)  # Highlighted
            pygame.draw.rect(self.screen, (255, 255, 255), self.button_rect, 2, border_radius=10)  # White border
        else:
            pygame.draw.rect(self.screen, self.back_button_color, self.button_rect, border_radius=10)  # Normal

        button_text = self.button_font.render("Back", True, self.text_color)
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, button_text_rect)

        self.draw_coins()  # Llamar a la función para dibujar las monedas
        pygame.display.flip()

    def run(self):
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
                        self.selected_index = len(self.characters)  # Select the "Back" button
                    elif event.key == pygame.K_UP:
                        if self.selected_index == len(self.characters):
                            self.selected_index = 0  # Navigate back to the first character
                    elif event.key == pygame.K_RETURN:
                        if self.selected_index == len(self.characters):
                            return  # Return to the previous menu (MenuView)
                        else:
                            selected_character = self.characters[self.selected_index]
                            if selected_character in self.unlocked_characters:
                                print(f"{selected_character} selected!")  # Mensaje de selección
                                return selected_character  # Retorna el personaje desbloqueado para jugar
                            else:
                                # Navigate to the store
                                print("Navigating to the store...")
                                return "store"  # Indica que se debe navegar a la tienda
                    elif event.key == pygame.K_ESCAPE:
                        return  # Act as the back button
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.button_rect.collidepoint(event.pos):
                            return  # Return to the previous menu (MenuView)

            self.draw()
            self.clock.tick(30)