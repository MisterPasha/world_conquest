import pygame
from button import Button

pygame.init()


class Country:
    country_button_image = pygame.image.load("images\\country_button.png")

    def __init__(self, screen, image, name):
        self.country_name = name
        self.owner = None
        self.troops = 0
        self.screen = screen

        self.plain_image = pygame.transform.scale(
            image, (screen.get_width(), screen.get_height())
        )

        self.image = self.plain_image
        self.color = (192, 192, 192)
        self.country_btn = self.set_button()
        # Separate image of when country needs to be highlighted
        self.image_highlighted = self.image
        # When True country is Highlighted
        self.highlighted = False

    # Draws a country image with appropriate color
    def draw(self):
        self.screen.blit(
            self.image_highlighted, (0, 0)
        ) \
            if self.highlighted else self.screen.blit(self.image, (0, 0))
        self.country_btn.draw(self.screen)

    def get_name(self):
        return self.country_name

    # Sets a new owner for this country
    def set_owner(self, new_owner):
        self.highlighted = False
        self.owner = new_owner
        self.set_color()
        self.set_button_color()
        color = pygame.Color(self.color)
        self.image = self.fill_with_color(self.plain_image, color)
        self.set_highlight_color()

    # Sets an owner's color
    def set_color(self):
        self.color = self.owner.get_color()

    # Pretty obvious...
    def add_troops(self, num_troops):
        self.troops += num_troops
        self.country_btn.change_text(str(self.troops))

    # Let me guess? removes one troop from the country...
    def remove_troops(self, num_troops):
        self.troops -= num_troops
        self.country_btn.change_text(str(self.troops))

    # function that fills countries with color
    def fill_with_color(self, image, color):
        coloured_image = pygame.Surface(self.image.get_size())
        coloured_image.fill(color)
        final_image = image.copy()
        final_image.blit(coloured_image, (0, 0), special_flags=pygame.BLEND_MULT)
        return final_image

    # finds a middle pixel of the country
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

    # creates a country button
    def set_button(self):
        x, y = self.find_country_middle()
        size = self.screen.get_height() * 0.05
        new_color = tuple(color - 20 for color in self.color)
        color = pygame.Color(new_color)
        btn = self.fill_with_color(self.country_button_image, color)
        button = Button(
            btn,
            btn,
            (x - size / 2, y - size / 2),
            str(self.troops),
            int(size * 0.8),
            size,
            size,
            hover=False,
        )
        return button

    # Sets a country button with a color of the country, but a little bit darker
    def set_button_color(self):
        new_color = tuple(color - 20 for color in self.color)
        color = pygame.Color(new_color)
        new_btn_color = self.fill_with_color(self.country_button_image, color)
        self.country_btn.change_image(new_btn_color)

    # Sets a color of the country when highlighted
    def set_highlight_color(self):
        yellow = (206, 222, 100)
        pink = (201, 171, 198)
        brown = (184, 149, 95)
        green = (84, 199, 153)
        red = (168, 69, 67)
        blue = (57, 108, 196)
        new_color = ()
        if self.color == yellow:
            new_color = (233, 250, 2)
        elif self.color == pink:
            new_color = (240, 117, 227)
        elif self.color == brown:
            new_color = (194, 111, 39)
        elif self.color == green:
            new_color = (2, 247, 149)
        elif self.color == red:
            new_color = (247, 5, 5)
        elif self.color == blue:
            new_color = (15, 4, 179)
        color_highlighted = pygame.Color(new_color)
        self.image_highlighted = self.fill_with_color(self.image, color_highlighted)

    # Checks clicks for country button
    def check_click(self, event):
        self.country_btn.check_click(event)


class Continent:
    def __init__(self, name):
        self.name = name
        self.list_of_countries = []

    def add_countries(self, countries):
        self.list_of_countries = countries
