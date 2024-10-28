import pygame

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load('assets/images/background_game.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

    def draw_background(self):
        self.screen.blit(self.background_image, (0, 0))

    def show_score(self, score):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_time(self, start_time):
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        font = pygame.font.Font(None, 36)
        time_text = font.render(f'{minutes:02}:{seconds:02}', True, (255, 255, 255))
        time_rect = time_text.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(time_text, time_rect)

    def show_upgrade_options(self, options, selected_option):
        # Dibujar una superposición semi-transparente
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Establecer nivel de transparencia
        self.screen.blit(overlay, (0, 0))
        upgrade_font = pygame.font.Font(None, 74)
        option_texts = [upgrade_font.render(option.name, True, (255, 255, 255)) for option in options]
        option_rects = [text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 100)) for i, text in enumerate(option_texts)]
        for rect, text in zip(option_rects, option_texts):
            self.screen.blit(text, rect)