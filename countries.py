import pygame  # Import the pygame library for game development
from button import Button  # Importing Button class

# Initialize pygame
pygame.init()


class Country:
    # The button image for country selection
    country_button_image = pygame.image.load("images\\country_button.png")

    def __init__(self, screen, image, name):
        """
        Initializes a country object
        :param screen: The Pygame screen surface
        :param image: The image representing the country
        :param name: The name of the country
        """
        self.country_name = name
        self.owner = None
        self.troops = 0
        self.screen = screen

        # Scale the image to match the screen size
        self.plain_image = pygame.transform.scale(
            image, (screen.get_width(), screen.get_height())
        )
        self.image = self.plain_image

        # Default colour for the country
        self.color = (192, 192, 192)

        # The country select button
        self.country_btn = self.set_button()

        # Separate image of when country needs to be highlighted
        self.image_highlighted = self.image

        # When True country is Highlighted
        self.highlighted = False

    def draw(self):
        """
        Draws a country image with appropriate color
        :return: [NONE]
        """
        self.screen.blit(
            self.image_highlighted, (0, 0)
        ) \
            if self.highlighted else self.screen.blit(self.image, (0, 0))
        # Draw the country button on the screen
        self.country_btn.draw(self.screen)

    def get_name(self):
        """
        Retrieve the name of the country
        :return: The name of the country 'self.country_name'
        """
        return self.country_name

    # Sets a new owner for this country
    def set_owner(self, new_owner):
        """
        Set the owner of the country
        :param new_owner: The certain player
        :return: [NONE]
        """
        self.highlighted = False
        self.owner = new_owner
        self.set_color()
        self.set_button_color()
        color = pygame.Color(self.color)
        self.image = self.fill_with_color(self.plain_image, color)
        self.set_highlight_color()

    def set_color(self):
        """
        Sets an owner's colour
        :return: [NONE]
        """
        self.color = self.owner.get_color()

    # Pretty obvious...
    def add_troops(self, num_troops):
        """
        Add troops to the country and update the button text with the new troop count
        :param num_troops: The number of troops to add
        :return: [NONE]
        """
        self.troops += num_troops
        self.country_btn.change_text(str(self.troops))

    # Let me guess? removes one troop from the country...
    def remove_troops(self, num_troops):
        """
        Remove troops from the country and update the button text with the new troop count
        :param num_troops: The number of troops to remove
        :return: [NONE]
        """
        self.troops -= num_troops
        self.country_btn.change_text(str(self.troops))

    def fill_with_color(self, image, color):
        """
        Function that fills countries with specified colour
        :param image: The original image to fill
        :param color: The colour to fill the image with
        :return: The new image with the specified colour 'final_image'
        """
        coloured_image = pygame.Surface(self.image.get_size())
        coloured_image.fill(color)
        final_image = image.copy()
        final_image.blit(coloured_image, (0, 0), special_flags=pygame.BLEND_MULT)
        return final_image

    def find_country_middle(self):
        """
        Ensure the image is in a format that supports per-pixel access.
        Finds a middle pixel of the country.
        :return: The coordinates of the middle pixel, or [NONE] if no non-transparent pixels are found.
        """
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
        """
        Creates a country button
        :return: The button for the country 'button'
        """
        # Find the middle pixel of the country
        x, y = self.find_country_middle()

        # Calculate the size of the button
        size = self.screen.get_height() * 0.05

        # Darken the color of the country for the button
        new_color = tuple(color - 20 for color in self.color)
        color = pygame.Color(new_color)

        # Create the button with the appropriate color and text
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

    def set_button_color(self):
        """
        Sets a country button with a colour of the country, but a little bit darker
        :return: [NONE]
        """
        new_color = tuple(color - 20 for color in self.color)
        color = pygame.Color(new_color)
        new_btn_color = self.fill_with_color(self.country_button_image, color)
        self.country_btn.change_image(new_btn_color)

    def set_highlight_color(self):
        """
        Sets a colour of the country when highlighted
        :return:
        """
        # Map specific colours to their highlighted versions
        color_map = {
            (206, 222, 100): (233, 250, 2),  # Yellow
            (201, 171, 198): (240, 117, 227),  # Pink
            (184, 149, 95): (194, 111, 39),  # Brown
            (84, 199, 153): (2, 247, 149),  # Green
            (168, 69, 67): (247, 5, 5),  # Red
            (57, 108, 196): (15, 4, 179)  # Blue
        }

        # Retrieve the highlighted colour based on the current color
        new_color = color_map.get(self.color)

        if new_color is not None:
            # Fill the country's image with the highlighted colour
            color_highlighted = pygame.Color(new_color)
            self.image_highlighted = self.fill_with_color(self.image, color_highlighted)

    def check_click(self, event):
        """
        Checks clicks for country button
        :param event:
        :return: [NONE]
        """
        self.country_btn.check_click(event)


class Continent:
    def __init__(self, name):
        """
        Initializes a Continent object with a given name
        :param name: The name of the continent
        """
        self.name = name
        self.list_of_countries = []

    def add_countries(self, countries):
        """
        Add a list of countries to the continent
        :param countries: The list of countries to add to the continent
        :return: [NONE]
        """
        self.list_of_countries = countries
