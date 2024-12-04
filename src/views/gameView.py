import pygame

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_width(), screen.get_height()
        self.scale_factor = self.HEIGHT / 1080
        self.background_image = pygame.image.load('assets/images/background_game.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        self.heart_image = pygame.image.load('assets/images/heart.png')
        self.heart_image = pygame.transform.scale(self.heart_image, (90, 90))  # Adjust the size of the heart
        self.upgrade_images = {}

        # Cargar fuentes
        self.font = pygame.font.Font('assets/fonts/pixel.ttf', int(36 * self.scale_factor))

    def draw_background(self):
        self.screen.blit(self.background_image, (0, 0))

    def show_score(self, score):
        score_text = self.font.render(f'Score: {score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_time(self, start_time):
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_text = self.font.render(f'{minutes:02}:{seconds:02}', True, (255, 255, 255))
        time_rect = time_text.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(time_text, time_rect)

    def show_health(self, health):
        for i in range(health):
            if health == 1 and (pygame.time.get_ticks() // 500) % 2 == 0:  # Blink every 500 ms
                continue  # Skip drawing the heart to create a blinking effect
            self.screen.blit(self.heart_image, (10 + i * 35, 50))  # Adjust the position of the hearts

    def show_upgrade_options(self, options, selected_option):
        # Dibujar una superposición semitransparente
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Establecer nivel de transparencia
        self.screen.blit(overlay, (0, 0))

        # Dibujar el título "LEVEL UP!"
        title_font = pygame.font.Font('assets/fonts/pixel.ttf', int(48 * self.scale_factor))
        title_text = title_font.render("LEVEL UP!", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, int(100 * self.scale_factor)))  # Posición ajustada
        self.screen.blit(title_text, title_rect)

        upgrade_font = pygame.font.Font('assets/fonts/pixel.ttf', int(36 * self.scale_factor))  # Tamaño de fuente ajustado
        option_texts = [upgrade_font.render(option.name, True, (255, 255, 255)) for option in options]

        # Precargar y escalar las imágenes de mejora
        upgrade_images = []
        for option in options:
            upgrade_image = pygame.image.load(option.image_path)
            image_rect = upgrade_image.get_rect()
            scale_factor = min(self.screen.get_width() // 4 / image_rect.width, self.screen.get_height() // 4 / image_rect.height)
            upgrade_image = pygame.transform.scale(upgrade_image, (int(image_rect.width * scale_factor), int(image_rect.height * scale_factor)))
            upgrade_images.append(upgrade_image)

        # Calcular las coordenadas iniciales x e y para centrar las opciones
        total_width = sum(image.get_width() for image in upgrade_images) + (len(upgrade_images) - 1) * int(150 * self.scale_factor)  # Separación ajustada
        start_x = (self.screen.get_width() - total_width) // 2
        start_y = self.screen.get_height() // 2

        for i, (text, upgrade_image) in enumerate(zip(option_texts, upgrade_images)):
            if i == selected_option:
                # Aumentar tamaño y mover hacia arriba la opción seleccionada
                upgrade_image = pygame.transform.scale(upgrade_image, (int(upgrade_image.get_width() * 1.2), int(upgrade_image.get_height() * 1.2)))
                image_rect = upgrade_image.get_rect(center=(start_x + upgrade_image.get_width() // 2, start_y - int(20 * self.scale_factor)))
            else:
                image_rect = upgrade_image.get_rect(center=(start_x + upgrade_image.get_width() // 2, start_y))

            self.screen.blit(upgrade_image, image_rect)

            # Dibujar el texto de mejora debajo de la imagen
            text_rect = text.get_rect(center=(image_rect.centerx, image_rect.bottom + int(80 * self.scale_factor)))  # Posición ajustada del texto
            self.screen.blit(text, text_rect)

            if i == selected_option:
                # Resaltar la opción seleccionada
                pygame.draw.rect(self.screen, (255, 255, 0), image_rect.inflate(int(20 * self.scale_factor), int(20 * self.scale_factor)), 3)  # Dibujar un rectángulo amarillo alrededor de la opción seleccionada

            start_x += upgrade_image.get_width() + int(150 * self.scale_factor)  # Mover a la siguiente posición con separación ajustada
    def show_chosen_upgrades(self, chosen_upgrades):
        start_y = 150  # Lower the starting y position
        for upgrade, count in chosen_upgrades.items():
            upgrade_image = self.upgrade_images[upgrade]
            upgrade_image.set_alpha(255)  # Set alpha to 100%
            for i in range(count):
                self.screen.blit(upgrade_image, (10 + i * 10, start_y))  # Shift each image slightly to the right
            start_y += upgrade_image.get_height() + 10

    def preload_upgrade_images(self, upgrades):
        for upgrade in upgrades:
            image = pygame.image.load(upgrade.image_path)
            image = self.scale_image(image, (50, 50))
            self.upgrade_images[upgrade.name] = image

    def scale_image(self, image, target_size):
        original_width, original_height = image.get_size()
        target_width, target_height = target_size

        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * aspect_ratio)

        scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))

        # Create a new surface with the target size and center the scaled image on it
        final_image = pygame.Surface(target_size, pygame.SRCALPHA)
        final_image.fill((0, 0, 0, 0))  # Fill with transparent color
        final_image.blit(scaled_image, ((target_width - new_width) // 2, (target_height - new_height) // 2))

        return final_image