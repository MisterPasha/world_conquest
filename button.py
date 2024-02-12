import pygame

pygame.init()


class Button:
    def __init__(self, image, pos, text, font_size, width, height, font=None, action=None):
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x, self.y = pos
        self.position = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.text = text
        self.font_size = font_size
        self.action = action
        self.font = pygame.font.Font(font, self.font_size)

    def draw(self, screen):
        # Draw the button image
        screen.blit(self.image, self.position)

        # Render the text
        text_surf = self.font.render(self.text, True, (0, 0, 0))  # Black text
        # Center the position of the text
        text_rect = text_surf.get_rect(center=self.rect.center)
        # Draw the text
        screen.blit(text_surf, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

    def change_image(self, new_image):
        new_image = pygame.transform.scale(new_image, (self.image.get_width(), self.image.get_height()))
        self.image = new_image
