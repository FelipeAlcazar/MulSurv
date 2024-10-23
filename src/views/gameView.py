import pygame

class GameView:
    def __init__(self, screen):
        self.screen = screen
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
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Set transparency level
        self.screen.blit(overlay, (0, 0))

        upgrade_font = pygame.font.Font(None, 74)
        option_texts = [upgrade_font.render(option.name, True, (255, 255, 255)) for option in options]
        option_rects = [text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 100)) for i, text in enumerate(option_texts)]

        for i, (text, rect) in enumerate(zip(option_texts, option_rects)):
            self.screen.blit(text, rect)
            if i == selected_option:
                pygame.draw.rect(self.screen, (0, 255, 0), rect, 3)