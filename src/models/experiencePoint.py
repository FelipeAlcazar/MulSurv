import pygame

class ExperiencePoint:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.size = 10
        self.image = pygame.image.load('assets/images/experience_point.png')
        self.image = pygame.transform.scale(self.image, (self.size * 3, self.size * 3))

    def draw(self, screen):
        screen.blit(self.image, (self.x - self.size, self.y - self.size))

    def move(self):
        pass  # Experience points don't move