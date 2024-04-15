import pygame  # Import the pygame library for game development

# Initialize pygame
pygame.init()
pygame.mixer.init()


class Button:
    def __init__(
            # To be initialized
            self,
            original_image,
            hover_image,
            pos,
            text,
            font_size,
            width,
            height,
            font=None,
            action=None,
            hover=True,
    ):
        """
        Initialize a Button object
        :param original_image: Surface of the button's original image
        :param hover_image: Surface of the button's image when hovered
        :param pos: Tuple representing the position of the button (x, y)
        :param text: Text to be displayed on the button
        :param font_size: Size of the font for the button text
        :param width: Width of the button
        :param height: Height of the button
        :param font: Font for the button text
        :param action: Function to be executed when the button is clicked
        :param hover: Boolean indicating whether hover effect is enabled
        """
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
        """
        Change image when cursor hovers button
        :param screen: Pygame screen surface
        :return: [NONE]
        """
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

    def check_click(self, event):
        """
        If click on self object is detected it triggers assigned function.
        Check if the button is clicked and execute its action if assigned
        :param event: Pygame event
        :return: [NONE]
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()

    # Changes current image to the new image
    def change_image(self, new_image):
        """
        Change the button's current image to a new image
        :param new_image: New image surface
        :return: [NONE]
        """
        new_image = pygame.transform.scale(
            new_image, (self.image.get_width(), self.image.get_height())
        )
        self.image = new_image

    def click(self, unclicked_image, clicked_image):
        """
        Specific feature for "Switch" type buttons.
        Toggle between clicked and unclicked states of the button
        :param unclicked_image: Image surface for unclicked state
        :param clicked_image: Image surface for clicked state
        :return: [NONE]
        """
        if self.clicked:
            self.image = pygame.transform.scale(
                unclicked_image, (self.image.get_width(), self.image.get_height())
            )
            self.clicked = False
        else:
            self.image = pygame.transform.scale(
                clicked_image, (self.image.get_width(), self.image.get_height())
            )
            self.clicked = True

    def change_text(self, new_text):
        """
        Change the text displayed on the button
        :param new_text: New text for the button
        :return: [NONE]
        """
        self.text = new_text

    def change_pos(self, new_x, new_y):
        """
        Changes Button position with new x and y
        :param new_x:
        :param new_y:
        :return:
        """
        self.position = (new_x, new_y)
        self.rect = self.image.get_rect(topleft=(new_x, new_y))

# Finished
