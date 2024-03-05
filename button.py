import pygame

pygame.init()

class Button:
    def __init__(self, original_image, hover_image, pos, text, font_size, width, height, font=None, action=None,
                 hover=True):
        self.original_image = pygame.transform.scale(original_image, (width, height))
        self.hover_image = pygame.transform.scale(hover_image, (width, height))
        self.image = self.original_image
        self.x, self.y = pos
        self.position = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.text = text
        self.font_size = font_size
        self.action = action
        self.font = pygame.font.Font(font, self.font_size)
        self.clicked = False
        self.hover_enabled = hover

    def draw(self, screen):
        # Change image when cursor hovers button
        if self.hover_enabled:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.hover_image
            else:
                self.image = self.original_image
        # Draw the button image
        screen.blit(self.image, self.position)
        # Render the text
        text_surf = self.font.render(self.text, True, (0, 0, 0))  # Black text
        # Center the position of the text
        text_rect = text_surf.get_rect(center=self.rect.center)
        # Draw the text
        screen.blit(text_surf, text_rect)

    # If click on self object is detected it triggers assigned function
    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()

    # Changes current image to the new image
    def change_image(self, new_image):
        new_image = pygame.transform.scale(new_image, (self.image.get_width(), self.image.get_height()))
        self.image = new_image

    # Specific feature for "Switch" type buttons
    def click(self, unclicked_image, clicked_image):
        if self.clicked:
            self.image = pygame.transform.scale(unclicked_image, (self.image.get_width(), self.image.get_height()))
            self.clicked = False
        else:
            self.image = pygame.transform.scale(clicked_image, (self.image.get_width(), self.image.get_height()))
            self.clicked = True

    def change_text(self, new_text):
        self.text = new_text
