import os
import pygame
import random

class Character:
    def __init__(self, x, y, size, speed, image_path, weapon):
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image_path)  # Use the image_path directly
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.red_tinted_image = self.image.copy()
        self.red_tinted_image.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
        self.weapon = weapon
        self.health = 2
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_duration = 3000  # 3 seconds of invincibility

        # Base path for assets
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")

        self.hit_sounds = [
            pygame.mixer.Sound(os.path.join(assets_path, "sounds", "playerHit.wav")), 
            pygame.mixer.Sound(os.path.join(assets_path, "sounds", "playerHit2.wav"))
        ]

    def draw(self, screen):
        if self.invincible:
            if (pygame.time.get_ticks() // 100) % 2 == 0:  # Blink every 100 ms
                screen.blit(self.red_tinted_image, (self.x, self.y))
                return  # Skip drawing the normal image to create a blinking effect
        screen.blit(self.image, (self.x, self.y))

    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            random.choice(self.hit_sounds).play()  # Randomly play one of the hit sounds

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < pygame.display.Info().current_w - self.size:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < pygame.display.Info().current_h - self.size:
            self.y += self.speed

    def update(self):
        if self.invincible and pygame.time.get_ticks() - self.invincible_start_time > self.invincible_duration:
            self.invincible = False