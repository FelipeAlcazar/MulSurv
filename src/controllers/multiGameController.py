import os
import sys
import time
import pygame
import socket
import threading
from src.models.rock import Rock
from src.models.tree import Tree
from src.models.projectile import Projectile
from src.views.characterSelectionView import CharacterSelectionView
from src.models.player import Player
import math
import random
from src.views.multiplayerEndGameView import MultiplayerEndGameView
import subprocess

class Game:
    def __init__(self, nickname, ip, port, start_server=True):
        pygame.init()
        
        if start_server:
            # Start the server
            self.start_server(ip, port)
        
        # Rest of the initialization code...
        pygame.init()
        
        # Start the server
        self.start_server(ip, port)
        
        # Obtener la resolución actual de la pantalla
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        
        # Inicialización de la ventana del juego
        self.win = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Multimedia Game")

        # Cargar imágenes
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")
        self.background_img = pygame.image.load(os.path.join(assets_path, "images", "background_game.png"))
        self.background_img = pygame.transform.scale(self.background_img, (screen_width, screen_height))

        # Configurar fuente para texto
        self.font = pygame.font.Font(None, 24)
        self.shots = {}

        # Variables del jugador y la red
        self.ip = ip
        self.port = port
        self.name = nickname
        self.user_id = 0
        self.is_live = 1
        self.score = 0
        self.cli_datas = []
        self.pointer_image = pygame.image.load(os.path.join(assets_path, "images", "pointer.png"))
        self.pointer_image = pygame.transform.scale(self.pointer_image, (20, 20))
        self.projectiles = []
        self.rocks = []
        self.trees = []
        rock_positions = [
            (250, 450), (600, 300), (850, 550), (900, 500),
            (410, 370), (730, 460), (1020, 250), (550, 600),
            (700, 520), (1100, 380)
        ]
        
        for pos in rock_positions:
            rock = Rock(screen_width, screen_height)
            rock.rect.x, rock.rect.y = pos
            self.rocks.append(rock)
        
        tree_positions = [
            (100, 100), (300, 500), (600, 700), (800, 200),
            (1200, 400), (1400, 600), (1600, 800), (1800, 300),
            (1500, 500), (1700, 700)
        ]
        
        for pos in tree_positions:
            tree = Tree(screen_width, screen_height)
            tree.rect.x, tree.rect.y = pos
            self.trees.append(tree)

        # Crear jugador
        self.player = None
        self.image_path = None
        self.select_character()
        self.send_join_request()
        
        self.wait_for_all_players()

        # Start network thread
        self.network_thread = threading.Thread(target=self.network_loop)
        self.network_thread.daemon = True
        self.network_thread.start()

        # Bucle principal del juego
        self.run()

    def start_server(self, ip, port):
        """Start the server as a subprocess."""
        base_path = os.path.dirname(__file__)
        server_path = os.path.join(base_path, 'serverController.py')
        if getattr(sys, 'frozen', False):
            # If the application is frozen (compiled with PyInstaller)
            server_path = os.path.join(sys._MEIPASS, 'src', 'controllers', 'serverController.py')
        subprocess.Popen(['python', server_path, '--host', ip, '--port', str(port)])
    
    def wait_for_all_players(self):
        """Wait for all players to be ready before starting the game."""
        waiting = True
        ready = False
        start_game = False
        ready_button_rect = pygame.Rect(
            (self.win.get_width() - 200) // 2,
            self.win.get_height() // 2 + 50,
            200,
            50
        )
        start_button_rect = pygame.Rect(
            (self.win.get_width() - 200) // 2,
            self.win.get_height() // 2 + 120,
            200,
            50
        )
        ready_button_color = (70, 70, 70)
        ready_button_hover_color = (90, 90, 90)
        ready_button_text_color = (255, 255, 255)
        
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")
        ready_button_font = pygame.font.Font(os.path.join(assets_path, "fonts", "pixel.ttf"), 36) 
        
        while waiting:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and ready_button_rect.collidepoint(event.pos):
                        ready = True
                        self.send_ready_status()
                    elif event.button == 1 and start_button_rect.collidepoint(event.pos) and self.user_id == 1 and self.all_players_ready():
                        start_game = True
                        self.send_start_game()  # Send start game message to the server

            self.win.fill((0, 0, 0))  # Dark background
            self.win.blit(self.background_img, (0, 0))

            # Display waiting message
            waiting_message = self.font.render("Waiting for all players...", True, (255, 255, 255))
            self.win.blit(waiting_message, waiting_message.get_rect(center=(self.win.get_width() // 2, self.win.get_height() // 2)))

            # Draw "Ready" button if not ready
            if not ready:
                if ready_button_rect.collidepoint(mouse_pos):
                    color = ready_button_hover_color
                else:
                    color = ready_button_color
                pygame.draw.rect(self.win, color, ready_button_rect, border_radius=10)
                ready_text = ready_button_font.render("Ready", True, ready_button_text_color)
                self.win.blit(ready_text, ready_text.get_rect(center=ready_button_rect.center))

            # Display player statuses
            player_statuses = self.get_player_statuses()
            for i, (player_name, is_ready) in enumerate(player_statuses):
                if is_ready:
                    status_text = self.font.render(f"{player_name} - Ready", True, (255, 255, 255))
                else:
                    status_text = self.font.render(f"{player_name}", True, (255, 255, 255))
                status_rect = status_text.get_rect(center=(self.win.get_width() // 2, self.win.get_height() // 2 - 100 + i * 30))
                self.win.blit(status_text, status_rect)

            # Check if all players are ready
            if self.all_players_ready() and len(player_statuses) > 1:
                all_ready_message = self.font.render("All players are ready!", True, (0, 255, 0))
                self.win.blit(all_ready_message, all_ready_message.get_rect(center=(self.win.get_width() // 2, self.win.get_height() // 2 + 100)))

                # Draw "Start Game" button if the current player is the host (user_id == 1)
                if self.user_id == 1:
                    if start_button_rect.collidepoint(mouse_pos):
                        color = ready_button_hover_color
                    else:
                        color = ready_button_color
                    pygame.draw.rect(self.win, color, start_button_rect, border_radius=10)
                    start_text = ready_button_font.render("Start Game", True, ready_button_text_color)
                    self.win.blit(start_text, start_text.get_rect(center=start_button_rect.center))

            # Check for start game signal from the server
            s = socket.socket()
            try:
                s.connect((self.ip, self.port))
                s.sendall("check_start".encode('utf-8'))
                response = s.recv(1024).decode("utf-8")
                s.close()
                if response == "start_game":
                    start_game = True
            except socket.error as msg:
                print(msg)

            pygame.display.update()

            if start_game:
                waiting = False  # Exit the waiting loop to start the game
    
    def send_start_game(self):
        """Send start game message to the server."""
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
            send_text = "start_game"
            s.sendall(send_text.encode('utf-8'))
            s.close()
        except socket.error as msg:
            print(msg)
        
    def get_player_statuses(self):
        """Get the status of all players from the server."""
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
            s.sendall("status_check".encode('utf-8'))
            response = s.recv(1024).decode("utf-8")
            s.close()
            if response:
                player_statuses = [tuple(player.split(":")) for player in response.split(";")]
                return [(name, status == "ready") for name, status in player_statuses]
            else:
                return [(self.name, False)]  # Return the current player's status if no other players are present
        except socket.error as msg:
            print(msg)
            return [(self.name, False)]  # Return the current player's status in case of an error
    


    def send_ready_status(self):
        """Send ready status to the server."""
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
            send_text = f"ready:{self.user_id}"
            s.sendall(send_text.encode('utf-8'))
            s.close()
        except socket.error as msg:
            print(msg)

    def send_join_request(self):
        """Send join request to the server."""
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
            send_text = f"join:{self.name}"
            s.sendall(send_text.encode('utf-8'))
            response = s.recv(1024).decode("utf-8")
            spl = response.split(":")
            if spl[0] == "id":
                self.user_id = int(spl[1])
            s.close()
        except socket.error as msg:
            print(msg)

    def all_players_ready(self):
        """Check if all players are ready."""
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
            s.sendall("ready_check".encode('utf-8'))
            response = s.recv(1024).decode("utf-8")
            s.close()
            return response == "all_ready"
        except socket.error as msg:
            print(msg)
            return False
    
    def send_pos(self):
        """Función para enviar posición al servidor."""
        s = socket.socket()
        try:
            s.connect((self.ip, self.port)) 
            send_text = f"pos:{self.name}:{self.player.x}:{self.player.y}:{self.player.image_path}:{self.user_id}"
            s.sendall(send_text.encode('utf-8'))
            yanit = s.recv(1024).decode("utf-8")
            
            if self.user_id == 0:
                spl = yanit.split(":")
                self.user_id = int(spl[1])
            else:
                self.cli_datas = yanit.split(";")

            s.close() 
        except socket.error as msg:
            print(msg)
            
    def receive_data(self):
        """Receive data from the server."""
        while True:
            s = socket.socket()
            try:
                s.connect((self.ip, self.port))
                s.sendall("check_start".encode('utf-8'))
                response = s.recv(1024).decode("utf-8")
                s.close()
                if response == "start_game":
                    self.run()
                    break  # Exit the loop after starting the game
            except socket.error as msg:
                print(msg)
            pygame.time.delay(30)  # Adjust delay as needed
            
    def select_character(self):
        """Muestra la pantalla de selección de personaje y asigna el personaje seleccionado."""
        selection_view = CharacterSelectionView(self.win)  # Usamos la misma pantalla
        while True:
            selected_character_name = selection_view.run()  # Mostramos la vista de selección de personajes
            if selected_character_name == "store":
                self.show_shop()
            elif selected_character_name:  # Si selecciona un personaje válido
                self.player = Player(character_name=selected_character_name)
                self.image_path = self.player.image_path
                screen_width, screen_height = self.win.get_width(), self.win.get_height()
                while True:
                    self.player.x = random.randint(0, screen_width - self.player.size)
                    self.player.y = random.randint(0, screen_height - self.player.size)
                    collision = False
                    for rock in self.rocks:
                        if self.check_collision_with_obstacles(self.player, rock.rect.x, rock.rect.y, rock.rect.width, rock.rect.height):
                            collision = True
                            break
                    for tree in self.trees:
                        if self.check_collision_with_obstacles(self.player, tree.rect.x, tree.rect.y, tree.rect.width, tree.rect.height):
                            collision = True
                            break
                    if not collision:
                        break
                break  # Salimos del bucle
            else:
                self.running = False  # Si no selecciona nada, salimos del juego
                return

    def send_shooting_coords(self, target_x, target_y):
        """Function to send shooting coordinates to the server."""
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
            send_text = f"shoot:{self.name}:{self.player.x}:{self.player.y}:{self.is_live}:{self.user_id}:{target_x}:{target_y}"
            s.sendall(send_text.encode('utf-8'))
            yanit = s.recv(1024).decode("utf-8")
            self.cli_datas = yanit.split(";")
            s.close()
        except socket.error as msg:
            print(msg)
            
    def network_loop(self):
        while True:
            self.send_pos()
            pygame.time.delay(30)  # Adjust delay as needed

    def draw_character_with_label(self, img, x, y, label):
        """Función para dibujar un personaje con texto encima."""
        self.win.blit(img, (x, y))
        text = self.font.render(label, True, (0, 0, 0))  # Texto en negro
        self.win.blit(text, (x + 5, y - 10))  # Posición del texto justo encima del personaje
        
    def draw_second_character_with_label(self, img, x, y, label):
        """Función para dibujar un personaje con texto encima."""
        image_surface = pygame.image.load(img)
        image_surface = pygame.transform.scale(image_surface, (50, 50))
        self.win.blit(image_surface, (x, y))
        text = self.font.render(label, True, (0, 0, 0))  # Texto en negro
        self.win.blit(text, (x + 5, y - 10))  # Posición del texto justo encima del personaje
        
    def shooting(self):
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
        self.win.blit(rotated_pointer, pointer_rect)

        # Adjust shooting to use the aiming position
        projectiles = self.player.shoot((aim_x, aim_y))

        if projectiles:
            if isinstance(projectiles, tuple):
                self.projectiles.extend(projectiles)
            else:
                self.projectiles.append(projectiles)

            # Send shooting coordinates to the server
            self.send_shooting_coords(aim_x, aim_y)

        for projectile in self.projectiles[:]:  # Iterate over projectiles
            projectile.move()  # Move each projectile
            projectile.draw(self.win)  # Draw each projectile
        
            if (projectile.x < 0 or projectile.x > self.win.get_width() or
                    projectile.y < 0 or projectile.y > self.win.get_height()):
                self.projectiles.remove(projectile)

    def display_shot(self, shooter_x, shooter_y, target_x, target_y):
        """Display the shot from another player."""
        shot_key = (shooter_x, shooter_y, target_x, target_y)
        
        current_time = pygame.time.get_ticks()
        
        # Debug statement to check if the shot is being processed
        #print(f"Processing shot: {shot_key} at time {current_time}")
        
        if shot_key not in self.shots or current_time - self.shots[shot_key] > 500:
            # Calculate angle between shooter and target position
            dx = target_x - (shooter_x + self.player.size // 2)
            dy = target_y - (shooter_y + self.player.size // 2)
            angle = math.atan2(dy, dx)

            # Calculate direction based on the angle
            direction_x = math.cos(angle)
            direction_y = math.sin(angle)

            # Create a projectile from the shooter's position
            projectile = Projectile(shooter_x + self.player.size // 2, shooter_y + self.player.size // 2, direction_x * 10, direction_y * 10)
            
            # Debug print statement to check the number of projectiles
            #print(f"Adding projectile at ({projectile.x}, {projectile.y}) with direction ({projectile.dx}, {projectile.dy})")
            
            # Ensure only one projectile is added
            self.projectiles.append(projectile)
            self.shots[shot_key] = current_time  # Store the shot with the current time

        # Remove old shots after half a second to prevent memory overflow
        self.shots = {key: time for key, time in self.shots.items() if current_time - time < 1000}
        # Debug statement to check the current shots dictionary
        #print(f"Current shots: {self.shots}")

    def draw_score(self):
        """Muestra el puntaje del jugador en la pantalla."""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.win.blit(score_text, (10, 10))

    
    def run(self):
        """Bucle principal del juego."""
        clock = pygame.time.Clock()
        run = True
        
        # Registrar el tiempo de inicio
        start_time = pygame.time.get_ticks()
        duration = 60 * 1000

        # Fuente para la cuenta regresiva
        font = pygame.font.Font(None, 36)  # Cambia el tamaño según lo necesites

        while run:
            clock.tick(60)  # Limitar la velocidad de fotogramas a 60 FPS
            
            # Calcular tiempo restante
            elapsed_time = pygame.time.get_ticks() - start_time
            remaining_time = max(0, duration - elapsed_time)  # Asegurarse de que no sea negativo
            seconds_left = remaining_time // 1000  # Convertir a segundos

            # Terminar el juego si el tiempo se acaba
            if remaining_time == 0:
                print("¡El tiempo ha terminado!")
                run = False

                # Request scores from the server
                s = socket.socket()
                try:
                    s.connect((self.ip, self.port))
                    send_text = f"end_game:{self.name}"
                    s.sendall(send_text.encode('utf-8'))
                    response = s.recv(1024).decode('utf-8')
                    s.close()
                    if response.startswith("end_game"):
                        scores_str = response.split(":")[1]
                        scores = {}
                        for item in scores_str.split(";"):
                            if "," in item:
                                player, score = item.split(",")
                                scores[player] = int(score)
                        MultiplayerEndGameView(self.win, scores).run()
                except socket.error as msg:
                    print(msg)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Control del movimiento del personaje
            keys = pygame.key.get_pressed()
            original_x, original_y = self.player.x, self.player.y
            self.player.move(keys)
            self.player.update()

            for rock in self.rocks:
                if self.check_collision_with_obstacles(self.player, rock.rect.x, rock.rect.y, rock.rect.width, rock.rect.height):
                    self.player.x, self.player.y = original_x, original_y  # Revert position if collision occurs

            for tree in self.trees:
                if self.check_collision_with_obstacles(self.player, tree.rect.x, tree.rect.y, tree.rect.width, tree.rect.height):
                    self.player.x, self.player.y = original_x, original_y
        
            # Dibujar el fondo primero
            self.win.blit(self.background_img, (0, 0))
            # Dibujar las piedras
            for rock in self.rocks:
                rock.draw(self.win)
            for tree in self.trees:
                tree.draw(self.win)
            self.shooting()

            self.draw_character_with_label(self.player.image, self.player.x, self.player.y, self.name)

            for projectile in self.projectiles:
                projectile.draw(self.win)

            # Dibujar otros personajes recibidos del servidor
            if self.cli_datas:
                for data in self.cli_datas:
                    if data != "0":
                        spl = data.split(":")
                        if spl[0] == "pos":
                            if int(spl[-1]) != self.user_id:
                                self.draw_second_character_with_label(spl[-2], int(spl[2]), int(spl[3]), spl[1])
                        elif spl[0] == "shoot":
                            if int(spl[5]) != self.user_id:
                                self.display_shot(int(spl[2]), int(spl[3]), float(spl[6]), float(spl[7]))

            # Detectar impactos de los proyectiles
            self.detect_impact()
            self.draw_score()

            # Dibujar la cuenta regresiva
            countdown_text = f"Tiempo restante: {seconds_left // 60}:{seconds_left % 60:02d}"
            text_surface = font.render(countdown_text, True, (255, 255, 255))  # Texto blanco
            self.win.blit(text_surface, (self.win.get_width() - text_surface.get_width() - 10, 10))  # Position on the top right corner

            pygame.display.update()

    def detect_impact(self):
        """Detecta los impactos de los proyectiles con las piedras, árboles y otros jugadores."""
        s = socket.socket()
        message = None  # Inicializar la variable message

        for projectile in self.projectiles[:]:  # Iterate over projectiles
            hit_detected = False  # Variable to track if a hit is detected

            for rock in self.rocks:
                if self.check_collision(projectile, rock.rect.x, rock.rect.y, rock.rect.width, rock.rect.height):
                    self.projectiles.remove(projectile)
                    hit_detected = True
                    break  # Exit the loop after detecting a collision

            if hit_detected:
                continue  # Skip checking other players if a rock collision is detected

            for tree in self.trees:
                if self.check_collision(projectile, tree.rect.x, tree.rect.y, tree.rect.width, tree.rect.height):
                    self.projectiles.remove(projectile)
                    hit_detected = True
                    break  # Exit the loop after detecting a collision

            if hit_detected:
                continue  # Skip checking other players if a tree collision is detected

            for data in self.cli_datas:
                if data != "0":
                    spl = data.split(":")
                    if spl[0] == "pos" and int(spl[-1]) != self.user_id:
                        shooter_x, shooter_y = int(spl[2]), int(spl[3])
                        if self.check_collision(projectile, shooter_x, shooter_y, self.player.size, self.player.size) and not self.is_projectile_too_new(projectile):
                            self.projectiles.remove(projectile)
                            message = f"hit:{self.user_id}"  # Asignar valor solo si hay colisión
                            hit_detected = True
                            break  # Exit the loop after detecting a collision

            if hit_detected:
                break  # Exit the loop after detecting a collision with a player

        if message:  # Solo intentar enviar si hay un mensaje
            try:
                s.connect((self.ip, self.port))
                s.sendall(message.encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                if response.startswith("score_update:"):
                    # Extraemos los datos usando el separador ":"
                    parts = response.split(":")
                    if len(parts) == 3:
                        shooter_id = parts[1]  # ID del jugador
                        score = int(parts[2])  # Score del jugador, convertido a entero
                        if shooter_id == str(self.user_id):  # Ensure the score update is for the current player
                            self.score = score  # Actualizamos el puntaje del jugador
                s.close()
            except socket.error as msg:
                print(msg)

    def is_projectile_too_new(self, projectile):
        # Check if the projectile is older than 100 milliseconds
        return time.time() - projectile.timestamp < 0.2

    def check_collision(self, projectile, x, y, width, height):
        collision = (projectile.x < x + width and
                    projectile.x + projectile.size > x and
                    projectile.y < y + height and
                    projectile.y + projectile.size > y)
        return collision
            
    def check_collision_with_obstacles(self, obj, x, y, width, height):
        """Check if an object collides with obstacles (rocks or trees)."""
        return (
            obj.x < x + width and
            obj.x + obj.size > x and
            obj.y < y + height and
            obj.y + obj.size > y
        )
    
    pygame.quit()