import pygame
import random

class Tree:
    def __init__(self, screen_width, screen_height):
        # Load images for different rock states
        self.image = pygame.image.load('assets/images/tree.png')
        self.state = 0  # Initial state
        self.rect = self.image.get_rect()

        # Random position within screen bounds
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        
        # Additional attributes for easy access to position and size
        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height
        self.size = self.rect.width  # Assuming the rock is square

    def draw(self, screen):
        # Draw the rock on the screen
        screen.blit(self.image, self.rect)
