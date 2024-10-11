import pygame
from src.models.character import Character
from src.models.projectile import Projectile
from src.models.weapon import Weapon

class Player(Character):
    predefined_characters = {
        "DefaultPlayer": {
            "image_path": 'assets/images/player_image.png',
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
        
        self.direction = pygame.K_RIGHT
        self.weapon = weapon
        self.last_shot = pygame.time.get_ticks()
        self.experience = 0
        self.level = 1
        self.experience_to_next_level = 100

    def move(self, keys):
        super().move(keys)
        if keys[pygame.K_LEFT]:
            self.direction = pygame.K_LEFT
        elif keys[pygame.K_RIGHT]:
            self.direction = pygame.K_RIGHT
        elif keys[pygame.K_UP]:
            self.direction = pygame.K_UP
        elif keys[pygame.K_DOWN]:
            self.direction = pygame.K_DOWN

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.weapon.shoot_delay:
            self.last_shot = now
            self.weapon.play_sound()
            if self.direction == pygame.K_LEFT:
                return Projectile(self.x, self.y + self.size // 2, -10, 0)
            elif self.direction == pygame.K_RIGHT:
                return Projectile(self.x + self.size, self.y + self.size // 2, 10, 0)
            elif self.direction == pygame.K_UP:
                return Projectile(self.x + self.size // 2, self.y, 0, -10)
            elif self.direction == pygame.K_DOWN:
                return Projectile(self.x + self.size // 2, self.y + self.size, 0, 10)
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