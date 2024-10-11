import pygame

class ExperiencePoint:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.size = 10

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.size)

    def move(self):
        pass  # Experience points don't move