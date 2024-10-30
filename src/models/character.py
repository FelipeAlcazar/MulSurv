import pygame

class Character:
    def __init__(self, x, y, size, speed, image_path, weapon):
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.weapon = weapon
        self.health = 2
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_duration = 3000  # 3 seconds of invincibility
        

    def draw(self, screen):
        if self.invincible:
            if (pygame.time.get_ticks() // 100) % 2 == 0:  # Blink every 100 ms
                return  # Skip drawing to create a blinking effect
        screen.blit(self.image, (self.x, self.y))


    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()

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
    
    