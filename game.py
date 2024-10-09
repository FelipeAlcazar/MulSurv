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
        self.experience = 0
        self.level = 1
        self.experience_to_next_level = 100

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

    def draw_experience_bar(self):
        bar_width = 200
        bar_height = 20
        fill = (self.experience / self.experience_to_next_level) * bar_width
        pygame.draw.rect(screen, WHITE, (10, 40, bar_width, bar_height), 2)
        pygame.draw.rect(screen, GREEN, (10, 40, fill, bar_height))

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
    def __init__(self, x, y, size, speed, image_path, experience):
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.experience = experience

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
        super().__init__(x, y, 40, 2, 'enemy_image.png', random.randint(10, 20))

# Clase para puntos de experiencia
class ExperiencePoint:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.size = 10

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.size)

    def move(self):
        pass  # Experience points don't move

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

    options = [play_rect, quit_rect]
    selected_option = 0

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        waiting = False
                    elif selected_option == 1:
                        pygame.quit()
                        exit()

        # Highlight selected option
        screen.fill(BLACK)
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)
        pygame.draw.rect(screen, GREEN, options[selected_option], 3)
        pygame.display.update()

# Función para mostrar opciones de mejora
def show_upgrade_options():
    upgrade_font = pygame.font.Font(None, 74)
    option1_text = upgrade_font.render("Upgrade 1", True, WHITE)
    option1_rect = option1_text.get_rect(center=(WIDTH // 2 - 300, HEIGHT // 2))
    option2_text = upgrade_font.render("Upgrade 2", True, WHITE)
    option2_rect = option2_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    option3_text = upgrade_font.render("Upgrade 3", True, WHITE)
    option3_rect = option3_text.get_rect(center=(WIDTH // 2 + 300, HEIGHT // 2))

    options = [option1_rect, option2_rect, option3_rect]
    selected_option = 0

    # Lower opacity of the game
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)  # Set transparency level
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Highlight selected option
    screen.blit(option1_text, option1_rect)
    screen.blit(option2_text, option2_rect)
    screen.blit(option3_text, option3_rect)
    pygame.draw.rect(screen, GREEN, options[selected_option], 3)
    pygame.display.update()

    return options, selected_option

# Juego principal
def main():
    show_menu()
    pygame.mouse.set_visible(False)
    player = Player(weapon="Sword")
    enemies = []
    projectiles = []
    experience_points = []
    spawn_indicators = []
    last_spawn_time = pygame.time.get_ticks()
    spawn_delay = 2000  # milliseconds
    blink_interval = 200  # milliseconds
    score = 0
    start_time = pygame.time.get_ticks()
    running = True
    upgrade_menu_active = False
    options = []
    selected_option = 0

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if upgrade_menu_active:
                    if event.key == pygame.K_RIGHT:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_LEFT:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        upgrade_menu_active = False

        if not upgrade_menu_active:
            # Movimiento del jugador
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.draw()
            player.draw_experience_bar()

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
                        score += 1
                        if random.random() < 0.5:  # 50% chance to drop experience
                            experience_points.append(ExperiencePoint(enemy.x, enemy.y, enemy.experience))
                        break

            # Movimiento y recolección de puntos de experiencia
            for exp in experience_points:
                exp.draw()
                if check_collision(player, exp):
                    player.experience += exp.value
                    experience_points.remove(exp)
                    if player.experience >= player.experience_to_next_level:
                        player.experience = 0
                        player.level += 1
                        upgrade_menu_active = True
                        options, selected_option = show_upgrade_options()

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

            # Mostrar puntaje
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {score}', True, WHITE)
            screen.blit(score_text, (10, 10))

            # Mostrar tiempo
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            time_text = font.render(f'{minutes:02}:{seconds:02}', True, WHITE)
            time_rect = time_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(time_text, time_rect)

        else:
            # Lower opacity of the game
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)  # Set transparency level
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            # Highlight selected option
            upgrade_font = pygame.font.Font(None, 74)
            option1_text = upgrade_font.render("Upgrade 1", True, WHITE)
            option1_rect = option1_text.get_rect(center=(WIDTH // 2 - 300, HEIGHT // 2))
            option2_text = upgrade_font.render("Upgrade 2", True, WHITE)
            option2_rect = option2_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            option3_text = upgrade_font.render("Upgrade 3", True, WHITE)
            option3_rect = option3_text.get_rect(center=(WIDTH // 2 + 300, HEIGHT // 2))

            options = [option1_rect, option2_rect, option3_rect]
            screen.blit(option1_text, option1_rect)
            screen.blit(option2_text, option2_rect)
            screen.blit(option3_text, option3_rect)
            pygame.draw.rect(screen, GREEN, options[selected_option], 3)

        # Actualizar la pantalla
        pygame.display.update()
        clock.tick(60)  # Controlar FPS

    pygame.quit()

if __name__ == "__main__":
    main()