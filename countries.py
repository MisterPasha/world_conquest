import pygame
from button import Button

pygame.init()


class Country:
    country_button_image = pygame.image.load("images\\country_button.png")

    def __init__(self, screen, image):
        self.country_name = ""
        self.owner = None
        self.troops = 0
        self.screen = screen
        self.image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
        self.color = (192, 192, 192)
        self.country_btn = self.set_button()

    def set_owner(self, new_owner):
        self.owner = new_owner

    def set_color(self):
        self.color = self.owner.get_color()

    def add_troops(self, num_troops):
        self.troops += num_troops

    def remove_troops(self, num_troops):
        self.troops -= num_troops

    def draw(self):
        color = pygame.Color(self.color)
        color_image = self.fill_with_color(self.image, color)
        self.screen.blit(color_image, (0, 0))
        self.country_btn.draw(self.screen)
        self.country_btn.change_text(str(self.troops))

    def fill_with_color(self, image, color):
        coloured_image = pygame.Surface(self.image.get_size())
        coloured_image.fill(color)

        final_image = image.copy()
        final_image.blit(coloured_image, (0, 0), special_flags=pygame.BLEND_MULT)
        return final_image

    def find_country_middle(self):
        # Ensure the image is in a format that supports per-pixel access
        if not self.image.get_locked():
            self.image.lock()

        width, height = self.image.get_size()
        min_x, min_y = width, height
        max_x, max_y = 0, 0

        # Scan pixels to find the bounding box of non-transparent parts
        for x in range(width):
            for y in range(height):
                alpha = self.image.get_at((x, y))[3]  # Get the alpha value of the pixel
                if alpha != 0:  # If the pixel is not transparent
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
        self.image.unlock()
        # If found some non-transparent pixels, calculate the middle
        if min_x < max_x and min_y < max_y:
            middle_x = (min_x + max_x) // 2
            middle_y = (min_y + max_y) // 2
            return middle_x, middle_y
        else:
            return None

    def set_button(self):
        x, y = self.find_country_middle()
        size = self.screen.get_height() * 0.05
        new_color = tuple(color - 20 for color in self.color)
        color = pygame.Color(new_color)
        btn = self.fill_with_color(self.country_button_image, color)
        button = Button(btn, btn, (x - size/2, y - size/2), str(self.troops), int(size * 0.8), size, size, hover=False)
        #self.country_btn = button
        return button

    def set_button_color(self):
        new_color = tuple(color - 20 for color in self.color)
        color = pygame.Color(new_color)
        new_btn_color = self.fill_with_color(self.country_button_image, color)
        self.country_btn.change_image(new_btn_color)

    def add_troop(self):
        self.troops += 1

    def check_click(self, event):
        self.country_btn.check_click(event)


class Continent:
    def __init__(self, name):
        self.name = name
        self.list_of_countries = []

    def add_countries(self, countries):
        self.list_of_countries = countries
