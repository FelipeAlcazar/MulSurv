import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, size, speed, image_path, experience):
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.experience = experience

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move_towards_player(self, player):
        direction_x = player.x - self.x
        direction_y = player.y - self.y
        distance = math.hypot(direction_x, direction_y)
        direction_x, direction_y = direction_x / distance, direction_y / distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

class SpecificEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 2, 'assets/images/enemy_image.png', random.randint(10, 20))