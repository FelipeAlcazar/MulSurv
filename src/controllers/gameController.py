import pygame
from src.models.player import Player
from src.models.enemy import SpecificEnemy
from src.models.experiencePoint import ExperiencePoint
from src.models.upgrade import available_upgrades
from src.utils.collision import check_collision
from src.views.gameView import GameView
from src.views.menuView import MenuView
import random
import math

class GameController:
    def __init__(self):
        self.init_display()
        self.clock = pygame.time.Clock()
        self.menu_view = MenuView(self.screen)
        self.game_view = GameView(self.screen)
        self.player = Player(character_name="DefaultPlayer")
        self.enemies = []
        self.projectiles = []
        self.experience_points = []
        self.spawn_indicators = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 2000  # Milisegundos, cambiará por nivel
        self.blink_interval = 200  # Milisegundos
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.running = True
        self.upgrade_menu_active = False
        self.options = []
        self.selected_option = 0
        self.level = 1  # Inicializar el nivel en 1
        self.enemies_to_defeat = 10  # Enemigos que deben ser eliminados por nivel
        self.enemies_defeated = 0  # Contador de enemigos derrotados

    def init_display(self):
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
        pygame.display.set_caption("Multimedia Game")

    def run(self):
        self.menu_view.show_menu()
        pygame.mouse.set_visible(False)

        while self.running:
            self.screen.fill((0, 0, 0))
            self.handle_events()
            if not self.upgrade_menu_active:
                self.update_game()
            else:
                self.game_view.show_upgrade_options(self.options, self.selected_option)
            pygame.display.update()
            self.clock.tick(60)  # Controlar FPS

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.upgrade_menu_active:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.apply_upgrade(self.options[self.selected_option])
                        self.upgrade_menu_active = False

    def update_game(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.draw(self.screen)
        self.player.draw_experience_bar(self.screen)

        projectile = self.player.shoot()
        if projectile:
            self.projectiles.append(projectile)

        for projectile in self.projectiles:
            projectile.move()
            projectile.draw(self.screen)

        for enemy in self.enemies:
            enemy.move_towards_player(self.player)
            enemy.draw(self.screen)

            if check_collision(self.player, enemy):
                print("¡Juego Terminado!")
                self.running = False

            for projectile in self.projectiles:
                if check_collision(projectile, enemy):
                    self.enemies.remove(enemy)
                    self.projectiles.remove(projectile)
                    self.enemies_defeated += 1  # Aumenta el contador de derrotas
                    self.score += 1

                    # Sistema de experiencia aleatorio
                    if random.random() < 0.7:  # 70% de probabilidad de soltar experiencia
                        exp_value = random.randint(0, 3)  # Entre 0 y 3 puntos de experiencia
                        if exp_value > 0:
                            self.experience_points.append(ExperiencePoint(enemy.x, enemy.y, exp_value))
                    break

        # Si se derrotaron suficientes enemigos, subir al siguiente nivel
        if self.enemies_defeated >= self.enemies_to_defeat:
            self.next_level()

        for exp in self.experience_points:
            exp.draw(self.screen)
            if check_collision(self.player, exp):
                self.player.experience += exp.value
                self.experience_points.remove(exp)
                if self.player.experience >= self.player.experience_to_next_level:
                    self.player.experience = 0
                    self.player.level += 1
                    self.upgrade_menu_active = True
                    self.options, self.selected_option = self.get_upgrade_options()

        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_delay:
            self.last_spawn_time = now
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                spawn_x = random.randint(0, self.screen.get_width() - 40)
                spawn_y = 0
            elif side == 'bottom':
                spawn_x = random.randint(0, self.screen.get_width() - 40)
                spawn_y = self.screen.get_height() - 40
            elif side == 'left':
                spawn_x = 0
                spawn_y = random.randint(0, self.screen.get_height() - 40)
            elif side == 'right':
                spawn_x = self.screen.get_width() - 40
                spawn_y = random.randint(0, self.screen.get_height() - 40)
            self.spawn_indicators.append((spawn_x, spawn_y, now, side))

        for indicator in self.spawn_indicators:
            spawn_x, spawn_y, spawn_time, side = indicator
            direction_x = self.player.x - spawn_x
            direction_y = self.player.y - spawn_y
            angle = math.degrees(math.atan2(direction_y, direction_x))
            arrow = pygame.image.load('assets/images/arrow.png')
            arrow = pygame.transform.rotate(arrow, -angle)
            arrow_rect = arrow.get_rect(center=(spawn_x + 20, spawn_y + 20))
            if (now // self.blink_interval) % 2 == 0:
                self.screen.blit(arrow, arrow_rect)
            if now - spawn_time > self.spawn_delay:
                self.enemies.append(SpecificEnemy(spawn_x, spawn_y))
                self.spawn_indicators.remove(indicator)

        self.game_view.show_score(self.score)
        self.game_view.show_time(self.start_time)

    def next_level(self):
        """Sube al siguiente nivel, ajusta dificultad y reinicia contadores."""
        self.level += 1
        self.enemies_defeated = 0
        self.enemies_to_defeat += 5  # Aumenta la cantidad de enemigos para el siguiente nivel
        self.spawn_delay = max(500, self.spawn_delay - 200)  # Aumenta la frecuencia de spawn

    def get_upgrade_options(self):
        # Seleccionar un subconjunto de mejoras disponibles
        options = random.sample(available_upgrades, 3)
        selected_option = 0
        return options, selected_option

    def apply_upgrade(self, upgrade):
        upgrade.apply(self.player)
