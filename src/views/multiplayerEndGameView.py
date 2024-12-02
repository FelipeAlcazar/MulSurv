import pygame
import time

class MultiplayerEndGameView:
    def __init__(self, win, scores):
        self.win = win
        self.scores = scores
        self.font = pygame.font.Font(None, 36)  # Base font size
        self.title_font = pygame.font.Font(None, 48)  # Font for the title
        self.blink = True
        self.last_blink_time = time.time()

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    run = False  # Exit the loop to return to the main menu

            self.win.fill((0, 0, 0))  # Clear screen with black

            # Display "scoreboard" title
            title_text = self.title_font.render("Scoreboard", True, (255, 255, 0))  # Yellow color
            self.win.blit(title_text, (self.win.get_width() // 2 - title_text.get_width() // 2, 50))

            # Display scores
            sorted_scores = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
            y_offset = 150
            for place, (player, score) in enumerate(sorted_scores, start=1):
                # Adjust font size based on place
                font_size = 48 - (place - 1) * 4  # Winner has the largest font, others decrease in size
                dynamic_font = pygame.font.Font(None, font_size)
                score_text = dynamic_font.render(f"{place}. {player}: {score}", True, (255, 255, 255))
                self.win.blit(score_text, (self.win.get_width() // 2 - score_text.get_width() // 2, y_offset))
                
                # Add blinking "WINNER" text next to the first place player
                if place == 1:
                    current_time = time.time()
                    if current_time - self.last_blink_time > 0.5:  # Toggle every 0.5 seconds
                        self.blink = not self.blink
                        self.last_blink_time = current_time
                    if self.blink:
                        winner_text = dynamic_font.render("WINNER", True, (255, 255, 0))  # Yellow color
                        self.win.blit(winner_text, (self.win.get_width() // 2 + score_text.get_width() // 2 + 10, y_offset))

                y_offset += 40

            # Indicate that pressing any key returns to the main menu
            info_text = self.font.render("Press any key to return to the main menu", True, (255, 255, 255))
            self.win.blit(info_text, (self.win.get_width() // 2 - info_text.get_width() // 2, y_offset + 20))

            pygame.display.update()