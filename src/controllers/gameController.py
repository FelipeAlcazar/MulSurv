import os
import pygame
from src.models.player import Player
from src.models.enemy import HeadphoneEnemy, MouseEnemy, SpecificEnemy, CameraEnemy, ControllerEnemy
from src.models.experiencePoint import ExperiencePoint
from src.models.upgrade import available_upgrades, decrease_speed
from src.views.characterSelectionView import CharacterSelectionView
from src.utils.collision import check_collision
from src.views.gameView import GameView
from src.views.shopView import ShopView
from src.utils.spawnManager import Spawner
from src.models.rock import Rock
from src.models.tree import Tree
from src.utils.data_manager import load_data, save_data
import random
import math
import time
from PIL import Image
from src.utils.scoreManager import ScoreManager
from src.views.pauseView import PauseView

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.init_display()
        self.reset_game()
        self.pause_view = PauseView(self.screen, self.options_font, self.pause_font)

    def reset_game(self):
        pygame.mouse.set_visible(False)
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")
        
        self.clock = pygame.time.Clock()
        self.game_view = GameView(self.screen)
        self.scoremanager = ScoreManager(self.screen)
        self.spawn_delay = 2000  # Milisegundos, cambiará con la dificultad
        self.spawner = Spawner(self.screen.get_width(), self.screen.get_height(), self.spawn_delay)
        self.arrow_image = pygame.image.load(os.path.join(assets_path, 'images', 'arrow.png'))
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.experience_points = []
        self.spawn_indicators = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.blink_interval = 200  # Milisegundos
        self.score = 0
        self.game_data = None
        self.coins = None
        self.start_time = None  # Initialize start_time as None
        self.running = True
        self.upgrade_menu_active = False
        self.options = []
        self.top_scores = None
        self.selected_option = 0
        self.pointer_image = pygame.image.load(os.path.join(assets_path, 'images', 'pointer.png'))
        self.pointer_image = pygame.transform.scale(self.pointer_image, (20, 20))
        self.enemy_switch_interval = 30000  # 30 seconds in milliseconds
        self.controller_enemy_interval = 60000  # 60 seconds in milliseconds
        self.paused = False
        self.chosen_upgrades = {}
        self.pause_font = pygame.font.Font(os.path.join(assets_path, 'fonts', 'pixel.ttf'), 74)
        self.options_font = pygame.font.Font(os.path.join(assets_path, 'fonts', 'pixel.ttf'), 48)
        
        # Cargar imagen de fondo
        self.background_image = pygame.image.load(os.path.join(assets_path, 'images', 'background_game.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

        # Preload upgrade images
        self.game_view.preload_upgrade_images(available_upgrades)

    def init_display(self):
        # Configuración inicial sin volver a crear la pantalla
        pygame.display.set_caption("Multimedia Game")

    def select_character(self):
        """Muestra la pantalla de selección de personaje y asigna el personaje seleccionado."""
        selection_view = CharacterSelectionView(self.screen)  # Usamos la misma pantalla
        while True:
            selected_character_name = selection_view.run()  # Mostramos la vista de selección de personajes
            if selected_character_name == "store":
                self.show_shop()
            elif selected_character_name:  # Si selecciona un personaje válido
                self.player = Player(character_name=selected_character_name)
                break  # Salimos del bucle
            else:
                self.running = False  # Si no selecciona nada, salimos del juego
                return

    def show_shop(self):
        """Muestra la pantalla de la tienda."""
        shop_view = ShopView(self.screen)  # Usamos la misma pantalla
        shop_view.run()

    def run(self):
        while True:
            self.select_character()  # Selección de personaje antes del juego
            if not self.player:
                return  # Return to menu if no character is selected
            self.start_time = pygame.time.get_ticks()  # Set start_time after character selection
            self.game_data = load_data()
            self.coins = self.game_data.get("coins", 0)
            self.unlocked_characters = self.game_data.get("unlocked_characters", [])
            self.rocks = []
            self.trees = []
            num_trees = random.randint(5, 10)
            num_rocks = random.randint(8, 20)
            for _ in range(num_rocks):
                while True:
                    rock = Rock(self.screen.get_width(), self.screen.get_height())
                    # Verificar que la roca no esté en la misma posición que el jugador
                    if not check_collision(self.player, rock):  # Implementar la función check_collision para verificar
                        self.rocks.append(rock)
                        break  # Salir del ciclo si la roca se genera en una posición válida
            for _ in range(num_trees):
                while True:
                    tree = Tree(self.screen.get_width(), self.screen.get_height())
                    # Verificar que el árbol no esté en la misma posición que el jugador
                    if not check_collision(self.player, tree):
                        self.trees.append(tree)
                        break

            if not self.player:
                self.running = False
                return
            pygame.mouse.set_visible(False)

            while self.running:
                self.screen.fill((0, 0, 0))

                self.screen.blit(self.background_image, (0, 0))

                # Lógica del juego y actualización de pantalla
                self.handle_events()
                if self.paused:
                    self.show_pause_menu()
                elif not self.upgrade_menu_active:
                    self.update_game()
                else:
                    self.game_view.show_upgrade_options(self.options, self.selected_option)

                pygame.display.update()
                self.clock.tick(60)

            self.end_game()
            return  # Return to menu after the game ends

    def end_game(self):
        """Finaliza el juego, muestra pantalla de Game Over con animación y texto, añade monedas ganadas y actualiza el scoreboard si es necesario."""
        self.coins += self.score

        # Add coins earned to the game data
        self.game_data["coins"] = self.coins

        # Save the score earned to the game data
        self.game_data["score_earned"] = self.score

        # Save the updated game data
        save_data(self.game_data)

        # Actualizar el scoreboard
        self.scoremanager.update_scoreboard(self.score)

        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")
        
        # Cargar y mostrar la pantalla de Game Over
        gif_path = os.path.join(assets_path, "images", "perder.gif")
        gif_frames = self.scoremanager.load_gif_frames(gif_path)

        # Cargar la imagen de fondo
        background_path = os.path.join(assets_path, "images", "background.png")
        background = self.scoremanager.load_background_image(background_path)

        # Cargar la imagen de Game Over
        game_over_image_path = os.path.join(assets_path, "images", "gameover.png")
        game_over_image = pygame.image.load(game_over_image_path)
        game_over_image = pygame.transform.scale(game_over_image, (500, 400))
        game_over_rect = game_over_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))

        # Mostrar la pantalla de Game Over
        self.scoremanager.show_game_over_screen(gif_frames, background, game_over_image, game_over_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused  # Toggle pause
                elif self.paused:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # "Resume" option
                            self.paused = False
                        elif self.selected_option == 1:  # "Quit" option
                            self.running = False
                elif self.upgrade_menu_active:
                    if event.key == pygame.K_LEFT:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.apply_upgrade(self.options[self.selected_option])
                        self.upgrade_menu_active = False

    def show_pause_menu(self):
        for rock in self.rocks:
            rock.draw(self.screen)
        for tree in self.trees:
            tree.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        for exp in self.experience_points:
            exp.draw(self.screen)
        self.game_view.show_score(self.score)
        self.game_view.show_time(self.start_time)
        self.game_view.show_health(self.player.health)
        self.game_view.show_chosen_upgrades(self.chosen_upgrades)
        self.pause_view.show(self.selected_option)

    def update_game(self):
        keys = pygame.key.get_pressed()
        original_x, original_y = self.player.x, self.player.y
        self.player.move(keys)

        for rock in self.rocks[:]:
            rock.draw(self.screen)
            if check_collision(self.player, rock):
                self.player.x, self.player.y = original_x, original_y  # Revert position if collision occurs
        
        for tree in self.trees[:]:
            tree.draw(self.screen)
            if check_collision(self.player, tree):
                self.player.x, self.player.y = original_x, original_y  # Revert position if collision occurs

        self.player.draw(self.screen)
        self.player.draw_experience_bar(self.screen)
        self.player.update()

        # Calculate angle between player and mouse position
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - (self.player.x + self.player.size // 2)
        dy = mouse_pos[1] - (self.player.y + self.player.size // 2)
        angle = math.atan2(dy, dx)

        # Restrict aiming to a circle around the player
        aim_radius = 45  # Radius of the aiming circle
        aim_x = self.player.x + self.player.size // 2 + math.cos(angle) * aim_radius
        aim_y = self.player.y + self.player.size // 2 + math.sin(angle) * aim_radius

        # Rotate pointer image
        rotated_pointer = pygame.transform.rotate(self.pointer_image, -math.degrees(angle) + 90)  # Adjust rotation to account for upward orientation

        # Position the pointer image at the aiming position
        pointer_rect = rotated_pointer.get_rect(center=(aim_x, aim_y))

        # Draw rotated pointer image
        self.screen.blit(rotated_pointer, pointer_rect)

        # Adjust shooting to use the aiming position
        projectiles = self.player.shoot((aim_x, aim_y))

        if projectiles:
            if isinstance(projectiles, tuple):
                self.projectiles.extend(projectiles)
            else:
                self.projectiles.append(projectiles)

        for projectile in self.projectiles[:]:  # Use a copy of the list to avoid issues when removing items
            projectile.move()
            projectile.draw(self.screen)

            # Check collisions between projectiles and rocks
            for rock in self.rocks[:]:
                if check_collision(projectile, rock):
                    if rock.take_damage():
                        self.rocks.remove(rock)  # Remove the rock if it is destroyed
                    self.projectiles.remove(projectile)  # Remove the projectile
                    break  # Exit the loop since the projectile has collided

        for enemy in self.enemies:
            enemy.move_towards_player(self.player)
            enemy.draw(self.screen)
            if check_collision(self.player, enemy):
                if not self.player.invincible:
                    if self.player.health == 1:
                        self.running = False
                    else:
                        self.player.take_damage()
                        self.enemies.remove(enemy)

            for projectile in self.projectiles[:]:  # Use a copy of the list
                if check_collision(projectile, enemy):
                    if enemy.take_damage():
                        self.enemies.remove(enemy)
                        self.score += 1
                        if random.random() < 0.7:
                            exp_value = random.randint(10, 30)
                            if exp_value > 0:
                                self.experience_points.append(ExperiencePoint(enemy.x, enemy.y, exp_value, pygame.time.get_ticks()))
                    self.projectiles.remove(projectile)
                    break

        # Optimize experience points handling
        for exp in self.experience_points[:]:
            if not exp.draw(self.screen):
                self.experience_points.remove(exp)
            elif check_collision(self.player, exp):
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

        enemy = self.spawner.spawn_enemy(elapsed_time)
        if enemy:
            self.enemies.append(enemy)

        self.game_view.show_score(self.score)
        self.game_view.show_time(self.start_time)
        self.game_view.show_health(self.player.health)
        self.game_view.show_chosen_upgrades(self.chosen_upgrades)

    def get_upgrade_options(self):
        excluded_upgrades = []
        if "Triple Shoot" in self.chosen_upgrades:
            excluded_upgrades.append("Triple Shoot")
            excluded_upgrades.append("Double Shoot")
        elif "Double Shoot" in self.chosen_upgrades:
            excluded_upgrades.append("Double Shoot")
    
        available_filtered_upgrades = [upgrade for upgrade in available_upgrades if upgrade.name not in excluded_upgrades]
        options = random.sample(available_filtered_upgrades, 3)
        
        for option in options:
            if option.name == "Enemies less aggressive":
                option.apply_upgrade = lambda player: decrease_speed(player, self.enemies)
        
        selected_option = 0
        return options, selected_option

    def apply_upgrade(self, upgrade):
        upgrade.apply(self.player)
        if upgrade.name in self.chosen_upgrades:
            self.chosen_upgrades[upgrade.name] += 1
        else:
            self.chosen_upgrades[upgrade.name] = 1