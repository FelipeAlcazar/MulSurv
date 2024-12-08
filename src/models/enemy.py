import os
import pygame
import random
import math

class Enemy:
    base_path = os.path.dirname(__file__)
    assets_path = os.path.join(base_path, "..", "..", "assets")

    predefined_enemies = {
        "DefaultEnemy": {
            "image_path": os.path.join(assets_path, "images", "floppy_disk_enemy.png"),
            "size": 50,
            "image_size": 50,
            "speed": 2,
            "health": 1
        },
        "CameraEnemy": {
            "image_path": os.path.join(assets_path, "images", "camera_enemy.png"),
            "size": 30,
            "image_size": 30,
            "speed": 3,
            "health": 2
        },
        "ControllerEnemy": {
            "image_path": os.path.join(assets_path, "images", "controller_enemy.png"),
            "size": 70,
            "image_size": 70,
            "speed": 4,
            "health": 3
        },
        "HeadphoneEnemy": {
            "image_path": os.path.join(assets_path, "images", "headphones.png"),
            "size": 50,
            "image_size": 50,
            "speed": 5,
            "health": 4
        },
        "MouseEnemy": {
            "image_path": os.path.join(assets_path, "images", "mouse.png"),
            "size": 80,
            "image_size": 80,
            "speed": 6,
            "health": 5
        }
    }

    def __init__(self, x, y, enemy_type="DefaultEnemy"):
        if enemy_type in self.predefined_enemies:
            enemy_info = self.predefined_enemies[enemy_type]
            self.size = enemy_info["size"]
            self.image_size = enemy_info["image_size"]
            self.speed = enemy_info["speed"]
            self.original_speed = self.speed
            self.health = enemy_info["health"]
            self.image = pygame.image.load(enemy_info["image_path"])
            self.image = pygame.transform.scale(self.image, (self.image_size, self.image_size))
        else:
            self.size = 40
            self.image_size = 60
            self.speed = 2
            self.original_speed = self.speed
            self.health = 1
            self.image = pygame.image.load(os.path.join(self.assets_path, "images", "enemy_image.png"))
            self.image = pygame.transform.scale(self.image, (self.image_size, self.image_size))
        
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
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
        self.health -= 1
        self.speed = max(1, self.speed - 1)  # Reduce speed but not below 1
        if self.health <= 0:
            return True  # Enemy should be removed
        return False  # Enemy is still alive

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