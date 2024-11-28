import pygame
import socket
import threading
from src.models.projectile import Projectile
from src.views.characterSelectionView import CharacterSelectionView
from src.models.player import Player
import math

class Game:
    def __init__(self, nickname):
        pygame.init()

        # Inicialización de la ventana del juego
        self.win = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Multimedia Game")

        # Cargar imágenes
        self.background_img = pygame.image.load("assets/images/background_game.png")  # Ruta a la imagen de fondo
        self.background_img = pygame.transform.scale(self.background_img, (800, 800))

        # Configurar fuente para texto
        self.font = pygame.font.Font(None, 24)  # Fuente predeterminada, tamaño 24

        # Variables del jugador y la red
        self.host = "localhost"
        self.port = 12345
        self.name = nickname
        self.user_id = 0
        self.is_live = 1
        self.cli_datas = []
        self.pointer_image = pygame.image.load('assets/images/pointer.png')  # Load pointer image
        self.pointer_image = pygame.transform.scale(self.pointer_image, (20, 20))  # Scale down pointer image
        self.projectiles = []

        # Crear jugador
        self.player = []
        self.select_character()


        # Start network thread
        self.network_thread = threading.Thread(target=self.network_loop)
        self.network_thread.daemon = True
        self.network_thread.start()

        # Bucle principal del juego
        self.run()

    def send_pos(self):
        """Función para enviar posición al servidor."""
        s = socket.socket()
        try:
            s.connect((self.host, self.port)) 
            send_text = f"pos:{self.name}:{self.player.x}:{self.player.y}:{self.is_live}:{self.user_id}"
            s.sendall(send_text.encode('utf-8'))
            yanit = s.recv(1024).decode("utf-8")
            
            if self.user_id == 0:
                spl = yanit.split(":")
                self.user_id = int(spl[-1])
                print(str(self.user_id))
            else:
                self.cli_datas = yanit.split(";")
            print("Data send_pos:"+yanit)
            
            s.close() 
        except socket.error as msg:
            print(msg)
            
            
    def select_character(self):
        """Muestra la pantalla de selección de personaje y asigna el personaje seleccionado."""
        selection_view = CharacterSelectionView(self.win)  # Usamos la misma pantalla
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


    def send_shooting_coords(self, target_x, target_y):
        """Function to send shooting coordinates to the server."""
        s = socket.socket()
        try:
            s.connect((self.host, self.port))
            send_text = f"shoot:{self.name}:{self.player.x}:{self.player.y}:{self.is_live}:{self.user_id}:{target_x}:{target_y}"
            s.sendall(send_text.encode('utf-8'))
            yanit = s.recv(1024).decode("utf-8")
            print("Data send_shooting_coords:" + yanit)
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

    def display_shot(self, shooter_x, shooter_y, target_x, target_y):
        """Display the shot from another player."""
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
        print(f"Adding projectile at ({projectile.x}, {projectile.y}) with direction ({projectile.dx}, {projectile.dy})")
        
        # Ensure only one projectile is added
        if projectile not in self.projectiles:
            self.projectiles.append(projectile)
    
    def run(self):
        """Bucle principal del juego."""
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)  # Limit frame rate to 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Control del movimiento del personaje
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.update()
            
            # Dibujar el fondo primero
            self.win.blit(self.background_img, (0, 0))
            self.shooting()

            # Dibujar el personaje principal si está vivo
            if self.is_live == 1:
                self.draw_character_with_label(self.player.image, self.player.x, self.player.y, self.name)
                
            for projectile in self.projectiles:
                projectile.draw(self.win)

            # Dibujar otros personajes recibidos del servidor
            if self.cli_datas != []:
                #print("Data from server: " + str(self.cli_datas))
                for i in self.cli_datas:
                    if i != "0":
                        spl = i.split(":")
                        #print("BEFORE CHECK: " + str(spl[-2]) + " " + str(spl[-1]) + " " + str(spl[0]) + " " + str(spl[1]) + " " + str(spl[2]) + " " + str(spl[3]) + " " + str(spl[4]))                            # Condition to not print the current player's info
                        if spl[0] == "pos":
                            #print("ALL DATA IN POS: " + str(spl[-2]) + " " + str(spl[-1]) + " " + str(spl[0]) + " " + str(spl[1]) + " " + str(spl[2]) + " " + str(spl[3]) + " " + str(spl[4]))                            # Condition to not print the current player's info
                            if int(spl[-1]) != self.user_id:
                                # Check if player is alive
                                if int(spl[-2]) != 0:
                                    self.draw_character_with_label(self.player.image, int(spl[2]), int(spl[3]), spl[1])
                        elif spl[0] == "shoot":
                            if int(spl[5]) != self.user_id:
                                print(f"ADDING SHOOT: {spl[2]} {spl[3]} {spl[6]} {spl[7]}")
                                self.display_shot(int(spl[2]), int(spl[3]), float(spl[6]), float(spl[7]))

            pygame.display.update() 

        pygame.quit()