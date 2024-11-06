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
                image_x = box_x + (box_width - character_image.get_width()) // 2
                self.screen.blit(character_image, (image_x, box_y + 10))

            # Nombre del personaje
            name_text = self.name_font.render(character_name, True, self.text_color)
            name_x = box_x + (box_width - name_text.get_width()) // 2
            self.screen.blit(name_text, (name_x, box_y + box_height // 2 + 20))
            
            character_costs = {
                "DefaultPlayer": 0,    # Por ejemplo, el personaje predeterminado es gratuito
                "Brillo": 500,
                "Mario": 50,
                "Miau Miau": 10000,
                # Agrega más personajes y sus costos aquí
            }

            # Mostrar estadísticas o costo si está bloqueado
            if character_name != "DefaultPlayer":
                cost = character_costs.get(character_name, 50)  # Obtener el costo del personaje, por defecto 50 si no está en el diccionario
                unlock_text = ""
                unlock_color = (255, 0, 0)  # Rojo si no se puede desbloquear
                if character_name in self.unlocked_characters:
                    unlock_text = "Unlocked"
                    unlock_color = (0, 255, 0)  # Verde si ya está desbloqueado
                else:
                    if self.coins >= cost:
                        unlock_text = f"Unlock for {cost} Coins"
                        unlock_color = (0, 255, 0)  # Verde si se puede desbloquear
                    else:
                        unlock_text = f"Locked (Cost: {cost} Coins)"

                unlock_text_render = self.unlock_font.render(unlock_text, True, unlock_color)
                self.screen.blit(unlock_text_render, (box_x + (box_width - unlock_text_render.get_width()) // 2, box_y + box_height // 2 + 40))
                if unlock_text != "Unlocked":  # Solo dibujar el candado si no está desbloqueado
                    self.screen.blit(self.locked_image, (box_x + box_width - 40, box_y + 10))

            # Nombre del arma
            weapon_name = character_data["weapon_name"]
            weapon_text = self.weapon_font.render(f"Weapon: {weapon_name}", True, self.text_color)
            weapon_x = box_x + (box_width - weapon_text.get_width()) // 2
            self.screen.blit(weapon_text, (weapon_x, box_y + box_height // 2 + 70))

            # Estadísticas del personaje
            stats_y = box_y + box_height // 2 + 100
            for stat, value in character_data.items():
                if stat not in ["image_path", "weapon_name"]:
                    stat_text = self.stats_font.render(f"{stat.capitalize()}: {value}", True, self.text_color)
                    self.screen.blit(stat_text, (box_x + 10, stats_y))
                    stats_y += 30

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
                        self.selected_index = (self.selected_index - 1) % len(self.characters)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.characters)
                    elif event.key == pygame.K_RETURN:
                        selected_character = self.characters[self.selected_index]
                        cost = 50  # Costo de desbloqueo

                        if self.unlocking:
                            # Si se ha desbloqueado un personaje y se presiona Enter, permitir la selección
                            print(f"{self.selected_character} selected!")  # Mensaje de selección
                            self.unlocking = False  # Reiniciar estado
                            return self.selected_character  # Retorna el personaje desbloqueado para jugar
                        elif selected_character in self.unlocked_characters:
                            # Si el personaje ya está desbloqueado, simplemente se selecciona
                            print(f"{selected_character} selected!")  # Mensaje de selección
                            return selected_character  # Retorna el personaje desbloqueado para jugar
                        else:
                            # Si no está desbloqueado, intenta desbloquearlo
                            if self.coins >= cost:
                                self.coins -= cost  # Descontar monedas
                                self.data["coins"] = self.coins  # Actualizar los datos
                                self.unlocked_characters.append(selected_character)  # Agregar personaje a desbloqueados
                                self.data["unlocked_characters"] = self.unlocked_characters  # Actualizar en el JSON
                                save_data(self.data)  # Guardar los cambios en el JSON
                                print(f"{selected_character} unlocked! Press Enter again to select.")  # Mensaje de desbloqueo
                                self.unlocking = True  # Cambia el estado a desbloqueando
                                self.selected_character = selected_character  # Guarda el personaje desbloqueado
                            else:
                                print("Not enough coins!")  # Mensaje de error

            self.draw()
            self.clock.tick(30)