import pygame

class MenuView:
    def __init__(self, screen):
        self.screen = screen

    def show_menu(self):
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        menu_font = pygame.font.Font(None, 74)
        play_text = menu_font.render("Play", True, (255, 255, 255))
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        quit_text = menu_font.render("Quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        self.screen.fill((0, 0, 0))
        self.screen.blit(play_text, play_rect)
        self.screen.blit(quit_text, quit_rect)
        pygame.display.update()

        options = [play_rect, quit_rect]
        selected_option = 0

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            waiting = False
                        elif selected_option == 1:
                            pygame.quit()
                            exit()

            self.screen.fill((0, 0, 0))
            self.screen.blit(play_text, play_rect)
            self.screen.blit(quit_text, quit_rect)
            pygame.draw.rect(self.screen, (0, 255, 0), options[selected_option], 3)
            pygame.display.update()