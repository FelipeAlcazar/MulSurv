import pygame
import random

class Rock:
    def __init__(self, screen_width, screen_height):
        # Cargar imagen de la roca
        self.image = pygame.image.load('assets/images/rock1.png')
        self.rect = self.image.get_rect()

        # Posición aleatoria dentro de los límites de la pantalla
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        
        # Atributos adicionales para facilitar el acceso a la posición y tamaño
        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height
        self.size = self.rect.width  # Asumimos que la roca es cuadrada, entonces el tamaño es el ancho

    def draw(self, screen):
        # Dibuja la roca en la pantalla
        screen.blit(self.image, self.rect)


