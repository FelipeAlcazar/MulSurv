import pygame
import random
import math

# Inicializamos Pygame
pygame.init()

# Dimensiones de la ventana del juego
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Simplified Vampire Survivors")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Clase base para personajes
class Character:
    def __init__(self, x, y, size, speed, image_path, weapon):
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.weapon = weapon

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.size:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.size:
            self.y += self.speed

# Clase jugador
class Player(Character):
    def __init__(self, weapon):
        super().__init__(WIDTH // 2, HEIGHT // 2, 60, 5, 'player_image.png', weapon)
        self.direction = pygame.K_RIGHT
        self.shoot_delay = 500  # milliseconds
        self.last_shot = pygame.time.get_ticks()

    def move(self, keys):
        super().move(keys)
        if keys[pygame.K_LEFT]:
            self.direction = pygame.K_LEFT
        elif keys[pygame.K_RIGHT]:
            self.direction = pygame.K_RIGHT
        elif keys[pygame.K_UP]:
            self.direction = pygame.K_UP
        elif keys[pygame.K_DOWN]:
            self.direction = pygame.K_DOWN

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.direction == pygame.K_LEFT:
                return Projectile(self.x, self.y + self.size // 2, -10, 0)
            elif self.direction == pygame.K_RIGHT:
                return Projectile(self.x + self.size, self.y + self.size // 2, 10, 0)
            elif self.direction == pygame.K_UP:
                return Projectile(self.x + self.size // 2, self.y, 0, -10)
            elif self.direction == pygame.K_DOWN:
                return Projectile(self.x + self.size // 2, self.y + self.size, 0, 10)
        return None

# Clase para proyectiles
class Projectile:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = 10

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))

# Clase base para enemigos
class Enemy:
    def __init__(self, x, y, size, speed, image_path):
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move_towards_player(self, player):
        direction_x = player.x - self.x
        direction_y = player.y - self.y
        distance = math.hypot(direction_x, direction_y)
        direction_x, direction_y = direction_x / distance, direction_y / distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

# Clase enemigo específico
class SpecificEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 2, 'enemy_image.png')

# Función para detectar colisiones
def check_collision(entity1, entity2):
    return (entity1.x < entity2.x + entity2.size and
            entity1.x + entity1.size > entity2.x and
            entity1.y < entity2.y + entity2.size and
            entity1.y + entity1.size > entity2.y)

# Función para mostrar el menú
def show_menu():
    menu_font = pygame.font.Font(None, 74)
    play_text = menu_font.render("Play", True, WHITE)
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    quit_text = menu_font.render("Quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.fill(BLACK)
    screen.blit(play_text, play_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    waiting = False
                elif quit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    waiting = False
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# Juego principal
def main():
    show_menu()
    player = Player(weapon="Sword")
    enemies = []
    projectiles = []
    spawn_indicators = []
    last_spawn_time = pygame.time.get_ticks()
    spawn_delay = 2000  # milliseconds
    blink_interval = 200  # milliseconds
    running = True

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw()

        # Disparar automáticamente
        projectile = player.shoot()
        if projectile:
            projectiles.append(projectile)

        # Movimiento de proyectiles
        for projectile in projectiles:
            projectile.move()
            projectile.draw()

        # Movimiento de enemigos
        for enemy in enemies:
            enemy.move_towards_player(player)
            enemy.draw()

            # Verificar colisión con el jugador
            if check_collision(player, enemy):
                print("¡Juego Terminado!")
                running = False

            # Verificar colisión con proyectiles
            for projectile in projectiles:
                if check_collision(projectile, enemy):
                    enemies.remove(enemy)
                    projectiles.remove(projectile)
                    break

        # Generar más enemigos con el tiempo
        now = pygame.time.get_ticks()
        if now - last_spawn_time > spawn_delay:
            last_spawn_time = now
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                spawn_x = random.randint(0, WIDTH - 40)
                spawn_y = 0
            elif side == 'bottom':
                spawn_x = random.randint(0, WIDTH - 40)
                spawn_y = HEIGHT - 40
            elif side == 'left':
                spawn_x = 0
                spawn_y = random.randint(0, HEIGHT - 40)
            elif side == 'right':
                spawn_x = WIDTH - 40
                spawn_y = random.randint(0, HEIGHT - 40)
            spawn_indicators.append((spawn_x, spawn_y, now, side))

        # Dibujar indicadores de spawn
        for indicator in spawn_indicators:
            spawn_x, spawn_y, spawn_time, side = indicator
            direction_x = player.x - spawn_x
            direction_y = player.y - spawn_y
            angle = math.degrees(math.atan2(direction_y, direction_x))
            arrow = pygame.image.load('arrow.png')
            arrow = pygame.transform.rotate(arrow, -angle)
            arrow_rect = arrow.get_rect(center=(spawn_x + 20, spawn_y + 20))
            if (now // blink_interval) % 2 == 0:  # Blink the arrow
                screen.blit(arrow, arrow_rect)
            if now - spawn_time > spawn_delay:
                enemies.append(SpecificEnemy(spawn_x, spawn_y))
                spawn_indicators.remove(indicator)

        # Actualizar la pantalla
        pygame.display.update()
        clock.tick(60)  # Controlar FPS

    pygame.quit()

if __name__ == "__main__":
    main()