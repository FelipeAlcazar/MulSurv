import os
import pygame
import time
from PIL import Image
from src.utils.data_manager import load_data, save_data

class ScoreManager:
    def __init__(self, screen):
        self.screen = screen
        self.game_data = load_data()
        self.top_scores = self.game_data.get("scoreboard", [])

    def update_scoreboard(self, score):
        """Verifica si el score entra en el top 3 y prepara la entrada para iniciales si lo hace."""
        # Si el puntaje es suficiente, añadirlo al top 3
        if len(self.top_scores) < 3 or score > self.top_scores[-1]["score"]:
            self.top_scores.append({"initials": "", "score": score})  # Añadir puntaje temporal
            self.top_scores = sorted(self.top_scores, key=lambda x: x["score"], reverse=True)[:3]

            # Solicitar iniciales del jugador
            initials = self.enter_initials()
            
            # Asignar las iniciales al puntaje
            for entry in self.top_scores:
                if entry["score"] == score and entry["initials"] == "":
                    entry["initials"] = initials
                    break

            # Guardar cambios en el scoreboard
            self.game_data["scoreboard"] = self.top_scores
            save_data(self.game_data)
            return None

    def enter_initials(self):
        """Pantalla para que el jugador ingrese sus iniciales y mostrar el top 3 actual."""
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")
        
        font_large = pygame.font.Font(os.path.join(assets_path, "fonts", "pixel.ttf"), 64)
        font_small = pygame.font.Font(os.path.join(assets_path, "fonts", "pixel.ttf"), 48)
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

    def load_gif_frames(self, gif_path):
        """Carga los fotogramas del GIF desde la ruta especificada."""
        gif = Image.open(gif_path)
        gif_frames = []

        try:
            while True:
                frame = gif.copy()
                # Convertir cada fotograma a un formato compatible con pygame
                frame = frame.convert("RGBA")
                pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                gif_frames.append(pygame_image)
                gif.seek(len(gif_frames))  # Ir al siguiente fotograma
        except EOFError:
            pass  # Termina cuando no hay más fotogramas

        return gif_frames

    def load_background_image(self, path):
        """Carga la imagen de fondo y la redimensiona."""
        base_path = os.path.dirname(__file__)
        assets_path = os.path.join(base_path, "..", "..", "assets")
        
        background = pygame.image.load(os.path.join(assets_path, path))
        background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
        background.set_alpha(80)  # Establecer opacidad
        return background

    def show_game_over_screen(self, gif_frames, background, game_over_image, game_over_rect):
        """Muestra la pantalla de 'Game Over' con la animación y los gráficos."""
        frame_index = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

            # Dibujar el fondo, el GIF y la imagen de "Game Over"
            self.screen.fill((0, 0, 0))  # Llenar con negro para asegurar que no haya artefactos
            self.screen.blit(background, (0, 0))  # Colocar la imagen de fondo
            gif_rect = gif_frames[frame_index].get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 1.5))
            self.screen.blit(gif_frames[frame_index], gif_rect)  # Colocar el GIF
            self.screen.blit(game_over_image, game_over_rect)  # Colocar la imagen de Game Over

            pygame.display.flip()  # Actualizar pantalla

            # Avanzar al siguiente fotograma
            frame_index = (frame_index + 1) % len(gif_frames)
            time.sleep(0.1)  # Controlar la velocidad de reproducción