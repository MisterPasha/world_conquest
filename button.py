import pygame
pygame.init()

hover_sound = pygame.mixer.Sound("C:\\Sussex\\Programming\\Software_Eng\\sounds\\button_click.wav")


def drop_colors(button_list, old_color, new_color):
    for button_ in button_list:
        if button_.color == old_color:
            button_.change_color(new_color)

class Button:
    BLACK = pygame.Color("black")

    def __init__(self, rect, color, hover_color, text, font_size, action, font=None):
        self.color = color
        self.hover_color = hover_color
        self.rect = rect
        self.text = text
        self.action = action
        self.hover = False
        self.was_hovered = False
        self.font_button = pygame.font.Font(font, font_size)

    # Function to draw a button
    def create_button(self, surface, width=0, br=-1, text_color=BLACK):
        color = self.hover_color if self.hover else self.color
        pygame.draw.rect(surface, color, self.rect, width=width, border_radius=br)
        text_surface = self.font_button.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.hover = True
            if not self.was_hovered:  # If it's the first time hovering
                hover_sound.play()  # Play sound
                self.was_hovered = True  # Update the flag so sound is not played again
        else:
            self.hover = False
            self.was_hovered = False  # Reset the flag when not hovering

    def check_click(self, mouse_pos):
        if self.hover:
            self.action()

    # changes a color of the button
    def change_color(self, new_color):
        self.color = new_color


