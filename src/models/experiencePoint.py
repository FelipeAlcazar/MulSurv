import pygame

class ExperiencePoint:
    # Class variable to hold the loaded and scaled image
    image = pygame.transform.scale(pygame.image.load('assets/images/experience_point.png'), (30, 30))

    def __init__(self, x, y, value, spawn_time):
        self.x = x
        self.y = y
        self.value = value
        self.size = 10
        self.spawn_time = spawn_time

    def draw(self, screen):
        now = pygame.time.get_ticks()
        elapsed_time = now - self.spawn_time

        if elapsed_time > 20000:
            return False  # Indicate that the experience point should be removed
        elif elapsed_time > 18000:
            if (now // 100) % 2 == 0:  # Blink every 100ms for the last 2 seconds
                screen.blit(self.image, (self.x - self.size, self.y - self.size))
        elif elapsed_time > 13000:
            if (now // 500) % 2 == 0:  # Blink every 500ms for 5 seconds
                screen.blit(self.image, (self.x - self.size, self.y - self.size))
        else:
            screen.blit(self.image, (self.x - self.size, self.y - self.size))
        
        return True  # Indicate that the experience point should still be drawn

    def move(self):
        pass  # Experience points don't move