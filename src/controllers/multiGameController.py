import threading
import pygame
from src.models.player import Player
from src.controllers.clientController import Client
from src.controllers.serverController import Server

class MultiPlayerGameController:
    def __init__(self, screen, is_server=False):
        self.screen = screen
        self.is_server = is_server
        self.client = Client()
        self.server = Server() if self.is_server else None
        self.client_id = None
        self.other_player = Player(character_name="DefaultPlayer")
        self.game_started = False
        self.running = True
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('assets/images/background_game.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        self.player = Player(character_name="DefaultPlayer")

        self.enemies = []
        self.projectiles = []
        self.experience_points = []
        self.rocks = []
        self.trees = []
        self.score = 0
        self.start_time = None

    def reset_game(self):
        self.player = Player(character_name="DefaultPlayer")
        self.other_player = Player(character_name="DefaultPlayer")
        self.enemies = []
        self.projectiles = []
        self.experience_points = []
        self.rocks = []
        self.trees = []
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        if self.is_server and self.server:
            server_thread = threading.Thread(target=self.server.run)
            server_thread.start()
        client_thread = threading.Thread(target=self.client.run)
        client_thread.start()

    def get_game_state(self):
        return {
            "client_id": self.client_id,
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "health": self.player.health,
                "experience": self.player.experience,
                "level": self.player.level
            },
            "other_player": {
                "x": self.other_player.x,
                "y": self.other_player.y,
                "health": self.other_player.health,
                "experience": self.other_player.experience,
                "level": self.other_player.level
            },
            "enemies": [{"x": enemy.x, "y": enemy.y, "health": enemy.health} for enemy in self.enemies],
            "projectiles": [{"x": proj.x, "y": proj.y} for proj in self.projectiles],
            "experience_points": [{"x": exp.x, "y": exp.y, "value": exp.value} for exp in self.experience_points]
        }

    def update_game_logic(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        for rock in self.rocks:
            rock.draw(self.screen)
        for tree in self.trees:
            tree.draw(self.screen)
        self.player.update()

    def update_game_view(self):
        game_state = self.client.game_state
        if not game_state:
            return

        self.screen.blit(self.background_image, (0, 0))

        self.other_player.x = game_state["other_player"]["x"]
        self.other_player.y = game_state["other_player"]["y"]
        self.other_player.draw(self.screen)

        self.player.x = game_state["player"]["x"]
        self.player.y = game_state["player"]["y"]
        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        for exp in self.experience_points:
            exp.draw(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run_multiplayer_game(self):
        while self.running:
            self.handle_events()
            if self.is_server:
                self.update_game_logic()
                self.client.send_message(self.get_game_state())
            else:
                self.client.send_message({"input": pygame.key.get_pressed()})
            self.update_game_view()
            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        pygame.init()
        self.reset_game()
        if self.is_server:
            server_game_thread = threading.Thread(target=self.run_multiplayer_game)
            server_game_thread.start()
        while self.running:
            self.run_multiplayer_game()
        pygame.quit()