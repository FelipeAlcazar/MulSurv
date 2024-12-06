import os
import pygame
import random

class Rock:
    def __init__(self, screen_width, screen_height):
        # Base path for assets
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")

        # Load images for different rock states
        self.images = [
            pygame.image.load(os.path.join(assets_path, "images", "rock1.png")),
            pygame.image.load(os.path.join(assets_path, "images", "rock2.png"))
        ]
        self.state = 0  # Initial state
        self.image = self.images[self.state]
        self.rect = self.image.get_rect()

        # Load a single hit sound
        self.hit_sound = pygame.mixer.Sound(os.path.join(assets_path, "sounds", "rockHit.wav"))

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

    def take_damage(self):
        # Play the hit sound
        self.hit_sound.play()
        
        # Change to the next state or mark for removal
        if self.state < len(self.images) - 1:
            self.state += 1
            self.image = self.images[self.state]
            self.rect = self.image.get_rect(center=self.rect.center)  # Update rect to keep the same center
            self.size = self.rect.width  # Update size to match new image
        else:
            return True  # Indicate that the rock should be removed
        return False