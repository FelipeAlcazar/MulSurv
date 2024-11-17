import pygame

class PauseView:
    def __init__(self, screen, options_font, pause_font):
        self.screen = screen
        self.options_font = options_font
        self.pause_font = pause_font


    def show(self, selected_option):
        """Muestra el menú de pausa."""
        grey_overlay = pygame.Surface(self.screen.get_size())
        grey_overlay.set_alpha(128)
        grey_overlay.fill((0, 0, 0))
        self.screen.blit(grey_overlay, (0, 0))

        options = ["Resume", "Quit"]
        pause_text = self.pause_font.render("Paused", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.screen.blit(pause_text, pause_rect)

        total_height = len(options) * self.options_font.get_height() + (len(options) - 1) * 20
        start_y = (self.screen.get_height() - total_height) // 2

        for i, option in enumerate(options):
            color = (255, 0, 0) if i == selected_option else (255, 255, 255)
            option_text = self.options_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.screen.get_width() // 2, start_y + i * (self.options_font.get_height() + 20)))
            self.screen.blit(option_text, option_rect)
        
