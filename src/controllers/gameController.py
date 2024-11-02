import pygame
from src.models.player import Player
from src.models.enemy import SpecificEnemy, CameraEnemy, ControllerEnemy
from src.models.experiencePoint import ExperiencePoint
from src.models.upgrade import available_upgrades, decrease_speed
from src.views.characterSelectionView import CharacterSelectionView 
from src.utils.collision import check_collision
from src.views.gameView import GameView
from src.views.menuView import MenuView
from src.utils.data_manager import load_data, save_data
import random
import math

class GameController:
    def __init__(self):
        self.init_display()
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.menu_view = MenuView(self.screen)
        self.game_view = GameView(self.screen)
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.experience_points = []
        self.spawn_indicators = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 2000  # Milisegundos, cambiará con la dificultad
        self.blink_interval = 200  # Milisegundos
        self.score = 0
        self.game_data = None
        self.coins = None
        self.start_time = pygame.time.get_ticks()
        self.running = True
        self.upgrade_menu_active = False
        self.options = []
        self.top_scores = None
        self.selected_option = 0
        self.pointer_image = pygame.image.load('assets/images/pointer.png')  # Load pointer image
        self.pointer_image = pygame.transform.scale(self.pointer_image, (20, 20))  # Scale down pointer image
        self.enemy_switch_interval = 30000  # 30 seconds in milliseconds
        self.controller_enemy_interval = 60000  # 60 seconds in milliseconds
        self.paused = False

        # Cargar imagen de fondo
        self.background_image = pygame.image.load('assets/images/background_game.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

    def init_display(self):
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
        pygame.display.set_caption("Multimedia Game")


    def select_character(self):
        """Muestra la pantalla de selección de personaje y asigna el personaje seleccionado."""
        selection_view = CharacterSelectionView(self.screen)
        selected_character_name = selection_view.run()
        if selected_character_name:
            self.player = Player(character_name=selected_character_name)

    def run(self):
        self.menu_view.show_menu()
        self.select_character()  # Selección de personaje antes del juego
        self.game_data = load_data()
        self.coins = self.game_data.get("coins", 0)
        self.top_scores = self.game_data.get("scoreboard", [])
        self.unlocked_characters = self.game_data.get("unlocked_characters", [])

        if not self.player:
            print("No character selected, exiting the game.")
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
        pygame.quit()

    
    def end_game(self):
        """Finaliza el juego, añade monedas ganadas y actualiza el scoreboard si es necesario."""
        self.coins += self.score
        print(f"Partida finalizada. Has ganado {self.score} monedas.")

        # Verificar si el score entra en el top 3
        if self.update_scoreboard(self.score):
            initials = self.enter_initials()
            # Actualizar la última entrada en el top 3 con las iniciales del jugador
            for entry in self.top_scores:
                if entry["score"] == self.score and entry["initials"] == "":
                    entry["initials"] = initials
                    break

        # Guardar cambios en JSON
        self.game_data["scoreboard"] = self.top_scores
        save_data(self.game_data)

    
    def update_scoreboard(self, score):
        """Verifica si el score entra en el top 3 y prepara la entrada para iniciales si lo hace."""
        # Añadir una entrada temporal con iniciales vacías si el score califica para el top 3
        if len(self.top_scores) < 3 or score > self.top_scores[-1]["score"]:
            self.top_scores.append({"initials": "", "score": score})  # Añadir puntaje temporal
            self.top_scores = sorted(self.top_scores, key=lambda x: x["score"], reverse=True)[:3]
            return True
        return False
    
    def enter_initials(self):
        """Pantalla para que el jugador ingrese sus iniciales y mostrar el top 3 actual."""
        font_large = pygame.font.Font(None, 64)
        font_small = pygame.font.Font(None, 48)
        initials = ""
        enter_initials = True

        while enter_initials:
            self.screen.fill((0, 0, 0))

            # Mostrar el top 3 actual en la parte superior de la pantalla
            scoreboard_text = font_large.render("Top 3 Scoreboard", True, (255, 255, 0))
            self.screen.blit(scoreboard_text, (self.screen.get_width() // 2 - scoreboard_text.get_width() // 2, 100))

            for i, entry in enumerate(self.top_scores):
                initials_text = entry["initials"] if entry["initials"] else "---"
                score_text = f"{initials_text}: {entry['score']}"
                score_display = font_small.render(score_text, True, (255, 255, 255))
                self.screen.blit(score_display, (self.screen.get_width() // 2 - score_display.get_width() // 2, 200 + i * 50))

            # Mostrar el prompt para ingresar las iniciales
            prompt_text = font_large.render("Enter Initials:", True, (255, 255, 255))
            initials_text = font_large.render(initials, True, (255, 255, 255))
            self.screen.blit(prompt_text, (self.screen.get_width() // 2 - prompt_text.get_width() // 2, 400))
            self.screen.blit(initials_text, (self.screen.get_width() // 2 - initials_text.get_width() // 2, 500))

            pygame.display.flip()

            # Procesar eventos de teclado para las iniciales
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    enter_initials = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(initials) == 3:
                        enter_initials = False  # Terminar entrada de iniciales
                    elif event.key == pygame.K_BACKSPACE and len(initials) > 0:
                        initials = initials[:-1]  # Borrar el último carácter
                    elif len(initials) < 3 and event.unicode.isalpha():
                        initials += event.unicode.upper()  # Añadir letra en mayúscula

        return initials if len(initials) == 3 else "AAA"


    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused  # Alternar pausa
                    elif self.paused:
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % 2
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % 2
                        elif event.key == pygame.K_RETURN:
                            if self.selected_option == 0:  # "Resume" opción
                                self.paused = False
                            elif self.selected_option == 1:  # "Quit" opción
                                self.running = False
                    elif self.upgrade_menu_active:
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            self.apply_upgrade(self.options[self.selected_option])
                            self.upgrade_menu_active = False
    
    def show_pause_menu(self):
        # Dibujar el fondo del menú de pausa
        pause_font = pygame.font.Font(None, 74)
        options_font = pygame.font.Font(None, 48)
        options = ["Resume", "Quit"]

        pause_text = pause_font.render("Paused", True, (255, 255, 255))
        self.screen.blit(pause_text, (self.screen.get_width() // 2 - pause_text.get_width() // 2, 150))

        for i, option in enumerate(options):
            color = (255, 0, 0) if i == self.selected_option else (255, 255, 255)
            option_text = options_font.render(option, True, color)
            self.screen.blit(option_text, (self.screen.get_width() // 2 - option_text.get_width() // 2, 300 + i * 60))


    def update_game(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.draw(self.screen)
        self.player.draw_experience_bar(self.screen)
        self.player.update()
        

        mouse_pos = pygame.mouse.get_pos()
        projectile = self.player.shoot(mouse_pos)
        
        self.player.draw_experience_bar(self.screen)
        
        if projectile:
            self.projectiles.append(projectile)

        for projectile in self.projectiles:
            projectile.move()
            projectile.draw(self.screen)

        for enemy in self.enemies:
            enemy.move_towards_player(self.player)
            enemy.draw(self.screen)
            if check_collision(self.player, enemy):
                if not self.player.invincible:
                    if self.player.health == 1:
                        print("¡Juego Terminado!")
                        self.running = False
                    else:
                        self.player.take_damage()
                        self.enemies.remove(enemy)
    
            for projectile in self.projectiles:
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
                elif elapsed_time < self.controller_enemy_interval:
                    enemy_type = CameraEnemy
                else:
                    enemy_type = ControllerEnemy
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
        self.game_view.show_health(self.player.health)

    def get_upgrade_options(self):
        options = random.sample(available_upgrades, 3)
        for option in options:
            if option.name == "Enemies less aggressive":
                option.apply_upgrade = lambda player: decrease_speed(player,self.enemies)
        selected_option = 0
        return options, selected_option

    def apply_upgrade(self, upgrade):
        upgrade.apply(self.player)