import pygame
from src.models.character import Character
from src.models.projectile import Projectile
from src.models.weapon import Weapon
import math

class Player(Character):
    predefined_characters = {
        "DefaultPlayer": {
            "image_path": 'assets/images/default_character.png',
            "weapon_name": "Gun",
            "size": 60,
            "speed": 5
        }
    }

    def __init__(self, character_name="DefaultPlayer"):
        info = pygame.display.Info()
        if character_name in self.predefined_characters:
            character_info = self.predefined_characters[character_name]
            weapon = Weapon(character_info["weapon_name"])
            super().__init__(info.current_w // 2, info.current_h // 2, character_info["size"], character_info["speed"], character_info["image_path"], weapon)
        else:
            weapon = Weapon("Gun")
            super().__init__(info.current_w // 2, info.current_h // 2, 60, 5, 'assets/images/player_image.png', weapon)
        
        self.direction = (0, 0)
        self.weapon = weapon
        self.last_shot = pygame.time.get_ticks()
        self.experience = 0
        self.level = 1
        self.experience_to_next_level = self.calculate_experience_to_next_level()

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
        self.x += dx * self.speed
        self.y += dy * self.speed

    def shoot(self, mouse_pos):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.weapon.shoot_delay:
            self.last_shot = now
            self.weapon.play_sound()
            # Calculate angle between player and mouse position
            dx = mouse_pos[0] - (self.x + self.size // 2)
            dy = mouse_pos[1] - (self.y + self.size // 2)
            angle = math.atan2(dy, dx)
            # Calculate direction based on angle
            direction_x = math.cos(angle)
            direction_y = math.sin(angle)
            return Projectile(self.x + self.size // 2, self.y + self.size // 2, direction_x * 10, direction_y * 10)
        return None

    def draw_experience_bar(self, screen):
        bar_width = 200
        bar_height = 20
        fill = (self.experience / self.experience_to_next_level) * bar_width
        pygame.draw.rect(screen, (255, 255, 255), (10, 40, bar_width, bar_height), 2)
        pygame.draw.rect(screen, (0, 255, 0), (10, 40, fill, bar_height))

    def change_weapon(self, new_weapon_name):
        self.weapon = Weapon(new_weapon_name)
        self.update_image()