import random
import pygame
from src.models.enemy import SpecificEnemy, CameraEnemy, ControllerEnemy, HeadphoneEnemy, MouseEnemy, PcEnemy

class Spawner:
    def __init__(self, screen_width, screen_height, spawn_delay):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_delay = spawn_delay
        self.last_spawn_time = pygame.time.get_ticks()
        self.pc_enemy_spawned = False

    def spawn_enemy(self, elapsed_time):
        if pygame.time.get_ticks() - self.last_spawn_time > self.spawn_delay:
            self.last_spawn_time = pygame.time.get_ticks()
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                spawn_x = random.randint(0, self.screen_width - 40)
                spawn_y = 0
            elif side == 'bottom':
                spawn_x = random.randint(0, self.screen_width - 40)
                spawn_y = self.screen_height - 40
            elif side == 'left':
                spawn_x = 0
                spawn_y = random.randint(0, self.screen_height - 40)
            elif side == 'right':
                spawn_x = self.screen_width - 40
                spawn_y = random.randint(0, self.screen_height - 40)

            # Lógica para seleccionar el tipo de enemigo según el tiempo
            enemy_type = self.select_enemy_type(elapsed_time)
            return enemy_type(spawn_x, spawn_y)
        return None

    def select_enemy_type(self, elapsed_time):
        if not self.pc_enemy_spawned and elapsed_time >= 270000:
            self.pc_enemy_spawned = True
            return PcEnemy
        elif elapsed_time < 30000:
            return SpecificEnemy
        elif elapsed_time < 60000:
            return CameraEnemy
        elif elapsed_time < 120000:
            return ControllerEnemy
        elif elapsed_time < 180000:
            return HeadphoneEnemy
        elif elapsed_time < 240000:
            return MouseEnemy
        elif elapsed_time >= 300000:
            return random.choice([SpecificEnemy, CameraEnemy, ControllerEnemy, HeadphoneEnemy, MouseEnemy])