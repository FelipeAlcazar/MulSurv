import pygame
import socket
from src.models.player import Player
import math

class Game:
    def __init__(self):
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
        self.name = "noname"
        self.user_id = 0
        self.is_live = 1
        self.cli_datas = []
        self.pointer_image = pygame.image.load('assets/images/pointer.png')  # Load pointer image
        self.pointer_image = pygame.transform.scale(self.pointer_image, (20, 20))  # Scale down pointer image
        self.projectiles = []
        
        # Crear jugador
        self.player = Player(character_name="DefaultPlayer")
        
        # Bucle principal del juego
        self.run()

    def send_pos(self):
        """Función para enviar posición al servidor."""
        s = socket.socket()
        try:
            s.connect((self.host, self.port)) 
            send_text = f"{self.name}:{self.player.x}:{self.player.y}:{self.is_live}:{self.user_id}"
            s.sendall(send_text.encode('utf-8'))
            yanit = s.recv(1024).decode("utf-8")
            if self.user_id == 0:
                spl = yanit.split(":")
                self.user_id = int(spl[-1])
                print(str(self.user_id))
            else:
                self.cli_datas = yanit.split(";")
            print(yanit)
            s.close() 
        except socket.error as msg:
            print(msg)

    def draw_character_with_label(self, img, x, y, label):
        """Función para dibujar un personaje con texto encima."""
        self.win.blit(img, (x, y))
        text = self.font.render(label, True, (0, 0, 0))  # Texto en negro
        self.win.blit(text, (x + 5, y - 10))  # Posición del texto justo encima del personaje
        
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)

        self.player.draw(self.win)
        self.player.draw_experience_bar(self.win)
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
        self.win.blit(rotated_pointer, pointer_rect)

        # Adjust shooting to use the aiming position
        projectiles = self.player.shoot((aim_x, aim_y))

        if projectiles:
            if isinstance(projectiles, tuple):
                self.projectiles.extend(projectiles)
            else:
                self.projectiles.append(projectiles)

        for projectile in self.projectiles[:]:  # Iterar sobre los proyectiles
            projectile.move()  # Mover cada proyectil
            projectile.draw(self.win)  # Dibujar cada proyectil


    def run(self):
        """Bucle principal del juego."""
        run = True
        while run:
            pygame.time.delay(100)
            self.send_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Control del movimiento del personaje
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.update()
            

            # Dibujar el fondo primero
            self.win.blit(self.background_img, (0, 0))
            self.update()

            # Dibujar el personaje principal si está vivo
            if self.is_live == 1:
                self.draw_character_with_label(self.player.image, self.player.x, self.player.y, "J1")
                self.player.draw_experience_bar(self.win)  # Dibujar la barra de experiencia encima
                
            for projectile in self.projectiles:
                projectile.draw(self.win)

            # Dibujar otros personajes recibidos del servidor
            if self.cli_datas != []:
                print(str(self.cli_datas))
                for i in self.cli_datas:
                    if i != "0":
                        spl = i.split(":")
                        if int(spl[-1]) != self.user_id:
                            if int(spl[-2]) != 0:
                                self.draw_character_with_label(self.player.image, int(spl[1]), int(spl[2]), "J2")

            pygame.display.update() 

        pygame.quit()