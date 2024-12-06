import os
import pygame
import random

class Tree:
    def __init__(self, screen_width, screen_height):
        # Base path for assets
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")

        # Load images for different tree states
        self.image = pygame.image.load(os.path.join(assets_path, "images", "tree.png"))
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
        self.size = self.rect.width  # Assuming the tree is square

    def draw(self, screen):
        # Draw the tree on the screen
        screen.blit(self.image, self.rect)