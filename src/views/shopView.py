import pygame
from src.models.player import Player
from src.utils.data_manager import load_data, save_data
import os

class ShopView:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Cargar datos de monedas y personajes desbloqueados
        self.data = load_data()
        self.coins = self.data.get("coins", 0)
        self.unlocked_characters = self.data.get("unlocked_characters", [])

        # Cargar imagen de la moneda y aumentar su tamaño
        self.coin_image = pygame.image.load("assets/images/coin.png").convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (48, 48))
        
        # Cargar imagen de candado
        self.locked_image = pygame.image.load("assets/images/lock.png").convert_alpha()
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
        self.selected_button = 0  # 0 para el botón "Volver", 1 para personajes
        
    def draw_coins(self):
        # Obtener el ancho de la pantalla
        screen_width = self.screen.get_width()
        
        # Calcular la posición x para que la imagen esté en la esquina superior derecha
        coin_x = screen_width - self.coin_image.get_width() - 100  # 100 píxeles de margen desde el borde derecho
        
        # Dibujar la imagen en la nueva posición
        coin_y = 10  # 10 píxeles de margen desde el borde superior
        self.screen.blit(self.coin_image, (coin_x, coin_y))
        
        # Dibujar el número de monedas al lado de la imagen
        font = pygame.font.Font(None, 36)
        coins_text = font.render(f"x {self.coins}", True, (255, 255, 255))
        
        # Asegurarse de que el texto esté alineado horizontalmente con la imagen
        text_y = coin_y + (self.coin_image.get_height() - coins_text.get_height()) // 2
        self.screen.blit(coins_text, (coin_x + self.coin_image.get_width() + 5, text_y))
        
    def draw(self):
        # Dibujar fondo
        self.screen.fill(self.background_color)

        # Título en mayúsculas
        title_text = pygame.font.Font(None, 48).render("TIENDA - COMPRAR PERSONAJES", True, self.text_color)
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
            if i == self.selected_index:
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
                image_x = box_x + (box_width - character_image.get_width()) // 2
                self.screen.blit(character_image, (image_x, box_y + 10))

            # Nombre del personaje
            name_text = pygame.font.Font(None, 24).render(character_name, True, self.text_color)
            name_x = box_x + (box_width - name_text.get_width()) // 2
            self.screen.blit(name_text, (name_x, box_y + box_height // 2 + 20))

            # Costo del personaje
            cost = character_data.get("cost", 50)  # Ejemplo de costo por defecto
            if character_name in self.unlocked_characters:
                unlock_text = "Desbloqueado"
                unlock_color = (0, 255, 0)
            else:
                unlock_text = f"Comprar por {cost} Monedas"
                unlock_color = (0, 255, 0) if self.coins >= cost else (255, 0, 0)

            unlock_text_render = pygame.font.Font(None, 20).render(unlock_text, True, unlock_color)
            self.screen.blit(unlock_text_render, (box_x + (box_width - unlock_text_render.get_width()) // 2, box_y + box_height // 2 + 40))

            if unlock_text != "Desbloqueado":
                self.screen.blit(self.locked_image, (box_x + box_width - 40, box_y + 10))

        # Botón de "Volver" en rojo
        back_button_rect = pygame.Rect(50, 10, 150, 50)
        if self.selected_button == 0:  # Si el botón "Volver" está seleccionado
            pygame.draw.rect(self.screen, (255, 0, 0), back_button_rect.inflate(10, 10), border_radius=10)  # Bordes agrandados para resaltar
        else:
            pygame.draw.rect(self.screen, self.back_button_color, back_button_rect, border_radius=10)  # Color rojo normal

        back_button_text = pygame.font.Font(None, 36).render("Volver", True, self.text_color)
        self.screen.blit(back_button_text, (back_button_rect.x + 10, back_button_rect.y + 10))

        self.draw_coins()
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si se hizo clic en el botón de "Volver"
            if pygame.Rect(50, 10, 150, 50).collidepoint(event.pos):
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
            elif event.key == pygame.K_RETURN:
                if self.selected_button == 0:  # Si se selecciona el botón "Volver"
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
                    running = False  # Salir si se pulsa el botón de "Volver"

            self.draw()
            self.clock.tick(30)