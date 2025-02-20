import os
import pygame
from src.models.character import Character
from src.models.projectile import Projectile
from src.models.weapon import Weapon
import math

class Player(Character):
    base_path = os.path.dirname(__file__)
    assets_path = os.path.join(base_path, "..", "..", "assets")

    predefined_characters = {
        "DefaultPlayer": {
            "image_path": os.path.join(assets_path, "images", "default_character.png"),
            "weapon_name": "Gun",
            "size": 50,
            "speed": 5,
            "cost": 0
        },
        "Mario": {
            "image_path": os.path.join(assets_path, "images", "second_character.png"),
            "weapon_name": "Gun",
            "size": 50,
            "speed": 7,
            "cost": 100
        },
        "Miau Miau": {
            "image_path": os.path.join(assets_path, "images", "personaje.png"),
            "weapon_name": "Gun",
            "size": 50,
            "speed": 9,
            "cost": 200
        },
        "Brillo": {
            "image_path": os.path.join(assets_path, "images", "Javi.png"),
            "weapon_name": "Gun",
            "size": 50,
            "speed": 6,
            "cost": 300
        },
        
    }

    def __init__(self, character_name="DefaultPlayer"):
        info = pygame.display.Info()
        if character_name in self.predefined_characters:
            character_info = self.predefined_characters[character_name]
            self.image_path = character_info["image_path"]
            weapon = Weapon(character_info["weapon_name"])
            super().__init__(info.current_w // 2, info.current_h // 2, character_info["size"], character_info["speed"], character_info["image_path"], weapon)
        else:
            weapon = Weapon("Gun")
            super().__init__(info.current_w // 2, info.current_h // 2, 60, 5, os.path.join(self.assets_path, "images", "player_image.png"), weapon)
        
        self.direction = (0, 0)
        self.weapon = weapon
        self.last_shot = pygame.time.get_ticks()
        self.experience = 0
        self.level = 1
        self.experience_to_next_level = self.calculate_experience_to_next_level()
        self.double_shoot = False
        self.triple_shoot = False

        # Load the pixel font
        self.font = pygame.font.Font(os.path.join(self.assets_path, "fonts", "pixel.ttf"), 36)

    def calculate_experience_to_next_level(self):
        # Experience required increases by 50% each level
        return 100 * (1.5 ** (self.level - 1))

    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        self.direction = (dx, dy)
        
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Get screen dimensions
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        
        # Ensure the player stays within the screen boundaries
        if 0 <= new_x <= screen_width - self.size:
            self.x = new_x
        if 0 <= new_y <= screen_height - self.size:
            self.y = new_y

    def shoot(self, mouse_pos):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.weapon.shoot_delay:
            self.last_shot = now
            self.weapon.play_sound()
            # Calcular el ángulo entre el jugador y la posición del ratón
            dx = mouse_pos[0] - (self.x + self.size // 2)
            dy = mouse_pos[1] - (self.y + self.size // 2)
            angle = math.atan2(dy, dx)
            # Calcular la dirección basada en el ángulo
            direction_x = math.cos(angle)
            direction_y = math.sin(angle)
            projectile1 = Projectile(self.x + self.size // 2, self.y + self.size // 2, direction_x * 10, direction_y * 10)
            
            if self.triple_shoot:
                self.double_shoot = False  # Desactivar doble disparo si triple disparo está activo
                angle_offset1 = 0.2  # Ajustar este valor para el spread deseado
                angle_offset2 = -0.2
                direction_x2 = math.cos(angle + angle_offset1)
                direction_y2 = math.sin(angle + angle_offset1)
                direction_x3 = math.cos(angle + angle_offset2)
                direction_y3 = math.sin(angle + angle_offset2)
                projectile2 = Projectile(self.x + self.size // 2, self.y + self.size // 2, direction_x2 * 10, direction_y2 * 10)
                projectile3 = Projectile(self.x + self.size // 2, self.y + self.size // 2, direction_x3 * 10, direction_y3 * 10)
                return (projectile1, projectile2, projectile3)
            
            if self.double_shoot:
                self.triple_shoot = False  # Desactivar triple disparo si doble disparo está activo
                angle_offset = 0.2  # Ajustar este valor para el spread deseado
                direction_x2 = math.cos(angle + angle_offset)
                direction_y2 = math.sin(angle + angle_offset)
                projectile2 = Projectile(self.x + self.size // 2, self.y + self.size // 2, direction_x2 * 10, direction_y2 * 10)
                return (projectile1, projectile2)
            
            return projectile1
        return None

    def draw_experience_bar(self, screen):
        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Draw player level
        level_text = self.font.render(f'Lvl. {self.level}', True, (255, 255, 255))
        level_text_rect = level_text.get_rect()
        bar_width = 200
        bar_height = 20
        level_text_x = (screen_width - level_text_rect.width) // 2
        level_text_y = screen_height - bar_height - level_text_rect.height - 20
        screen.blit(level_text, (level_text_x, level_text_y))

        # Draw experience bar
        fill = (self.experience / self.experience_to_next_level) * bar_width
        bar_x = (screen_width - bar_width) // 2
        bar_y = screen_height - bar_height - 10
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill, bar_height))

    def change_weapon(self, new_weapon_name):
        self.weapon = Weapon(new_weapon_name)
        self.update_image()