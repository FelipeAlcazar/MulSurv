import pygame
import random
import math

class Enemy:
    predefined_enemies = {
        "DefaultEnemy": {
            "image_path": 'assets/images/floppy_disk_enemy.png',
            "size": 50,
            "image_size": 50,
            "speed": 2
        },
        "CameraEnemy": {
            "image_path": 'assets/images/camera_enemy.png',
            "size": 30,
            "image_size": 30,
            "speed": 4
        },
        "ControllerEnemy": {
            "image_path": 'assets/images/controller_enemy.png',
            "size": 70,
            "image_size": 70,
            "speed": 3
        },
        "HeadphoneEnemy": {
            "image_path": 'assets/images/headphones.png',
            "size": 50,
            "image_size": 50,
            "speed": 4
        },
        "MouseEnemy": {
            "image_path": 'assets/images/mouse.png',
            "size": 80,
            "image_size": 80,
            "speed": 3
        }
    }

    def __init__(self, x, y, enemy_type="DefaultEnemy"):
        if enemy_type in self.predefined_enemies:
            enemy_info = self.predefined_enemies[enemy_type]
            self.size = enemy_info["size"]
            self.image_size = enemy_info["image_size"]
            self.speed = enemy_info["speed"]
            self.image = pygame.image.load(enemy_info["image_path"])
            self.image = pygame.transform.scale(self.image, (self.image_size, self.image_size))
        else:
            self.size = 40
            self.image_size = 60
            self.speed = 2
            self.image = pygame.image.load('assets/images/enemy_image.png')
            self.image = pygame.transform.scale(self.image, (self.image_size, self.image_size))
        
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        bounding_box = self.get_bounding_box()
        pygame.draw.rect(screen, (255, 0, 0), bounding_box, 2)  # Draw hitbox with red color and 2px thickness

    def move_towards_player(self, player):
        direction_x = player.x - self.x
        direction_y = player.y - self.y
        distance = math.hypot(direction_x, direction_y)
        direction_x, direction_y = direction_x / distance, direction_y / distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

    def get_bounding_box(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def take_damage(self):
        # Default behavior: remove enemy immediately
        return True

class SpecificEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "DefaultEnemy")

class CameraEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "CameraEnemy")

class HeadphoneEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "HeadphoneEnemy")

class MouseEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "MouseEnemy")

class ControllerEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "ControllerEnemy")
        self.health = 2  # Requires two shots to be killed

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            return True  # Enemy should be removed
        return False  # Enemy is still alive