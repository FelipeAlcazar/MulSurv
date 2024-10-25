import pygame
from src.models.player import Player
from src.models.enemy import SpecificEnemy, CameraEnemy
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
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.menu_view = MenuView(self.screen)
        self.game_view = GameView(self.screen)
        self.player = Player(character_name="DefaultPlayer")
        self.enemies = []
        self.projectiles = []
        self.experience_points = []
        self.spawn_indicators = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 2000  # Milisegundos, cambiará con la dificultad
        self.blink_interval = 200  # Milisegundos
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.running = True
        self.upgrade_menu_active = False
        self.options = []
        self.selected_option = 0
        self.pointer_image = pygame.image.load('assets/images/pointer.png')  # Load pointer image
        self.pointer_image = pygame.transform.scale(self.pointer_image, (20, 20))  # Scale down pointer image
        self.enemy_switch_interval = 30000  # 30 seconds in milliseconds

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
        pygame.mouse.set_visible(False)  # Ensure the mouse cursor is hidden
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.draw(self.screen)
        self.player.draw_experience_bar(self.screen)

        mouse_pos = pygame.mouse.get_pos()
        projectile = self.player.shoot(mouse_pos)
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
                    self.score += 1

                    if random.random() < 0.7:
                        exp_value = random.randint(10, 30)
                        if exp_value > 0:
                            self.experience_points.append(ExperiencePoint(enemy.x, enemy.y, exp_value))
                    break

        for exp in self.experience_points:
            exp.draw(self.screen)
            if check_collision(self.player, exp):
                self.player.experience += exp.value
                self.experience_points.remove(exp)
                if self.player.experience >= self.player.experience_to_next_level:
                    self.player.experience = 0
                    self.player.level += 1
                    self.player.experience_to_next_level = self.player.calculate_experience_to_next_level()
                    self.upgrade_menu_active = True
                    self.options, self.selected_option = self.get_upgrade_options()

        now = pygame.time.get_ticks()
        elapsed_time = now - self.start_time
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
                if elapsed_time < self.enemy_switch_interval:
                    enemy_type = SpecificEnemy
                else:
                    enemy_type = CameraEnemy
                self.enemies.append(enemy_type(spawn_x, spawn_y))
                self.spawn_indicators.remove(indicator)

        # Calculate angle between player and mouse position
        dx = mouse_pos[0] - (self.player.x + self.player.size // 2)
        dy = mouse_pos[1] - (self.player.y + self.player.size // 2)
        angle = math.degrees(math.atan2(dy, dx))

        # Rotate pointer image
        rotated_pointer = pygame.transform.rotate(self.pointer_image, -angle + 90)  # Adjust rotation to account for upward orientation

        # Position the pointer image further in front of the player
        pointer_distance = 50  # Increased distance from the player
        pointer_x = self.player.x + self.player.size // 2 + math.cos(math.radians(angle)) * pointer_distance
        pointer_y = self.player.y + self.player.size // 2 + math.sin(math.radians(angle)) * pointer_distance
        pointer_rect = rotated_pointer.get_rect(center=(pointer_x, pointer_y))

        # Draw rotated pointer image
        self.screen.blit(rotated_pointer, pointer_rect)

        self.game_view.show_score(self.score)
        self.game_view.show_time(self.start_time)

    def get_upgrade_options(self):
        options = random.sample(available_upgrades, 3)
        selected_option = 0
        return options, selected_option

    def apply_upgrade(self, upgrade):
        upgrade.apply(self.player)