import pygame  # Import the pygame library for game development
from button import Button  # Importing Button class
from main_menu import draw_text

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
        self.color = (250, 250, 250)

        # The country select button
        self.country_btn = self.set_button()

        # Separate image of when country needs to be highlighted
        self.image_highlighted = self.image
        self.set_highlight_color()

        # When True country is Highlighted
        self.highlighted = False

    def draw(self):
        """
        Draws a country image with appropriate color
        :return: [NONE]
        """
        self.screen.blit(
            self.image_highlighted, (0, 0)
        ) if self.highlighted else self.screen.blit(self.image, (0, 0))
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
        :return: The coordinates of the middle pixel ('middle_x, middle_y'), or [NONE] if no non-transparent pixels are found.
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
        :return: [NONE]
        """
        # Map specific colours to their highlighted versions
        color_map = {
            (206, 222, 100): (233, 250, 2),  # Yellow
            (201, 171, 198): (240, 117, 227),  # Pink
            (184, 149, 95): (194, 111, 39),  # Brown
            (84, 199, 153): (2, 247, 149),  # Green
            (168, 69, 67): (247, 5, 5),  # Red
            (57, 108, 196): (15, 4, 179),  # Blue
            (250, 250, 250): (150, 150, 150),  # Gray
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


def create_neighbours():
    """
    A dictionary of a country and its neighbours
    :return: 'dictionary' Neighbours
    """
    dictionary = {
        "Alaska": ["Northwest Territory", "Alberta", "Kamchatka"],

        "Alberta": ["Alaska", "Northwest Territory", "Ontario", "Western US"],

        "Central America": ["Venezuela", "Eastern US", "Western US"],

        "Eastern US": ["Central America", "Western US", "Ontario", "Quebec"],

        "Greenland": ["Iceland", "Quebec", "Ontario", "Northwest Territory"],

        "Northwest Territory": ["Alaska", "Alberta", "Ontario", "Greenland"],

        "Ontario": ["Northwest Territory", "Alberta", "Western US", "Eastern US", "Quebec", "Greenland"],

        "Quebec": ["Ontario", "Eastern US", "Greenland"],

        "Western US": ["Central America", "Eastern US", "Ontario", "Alberta"],

        "Argentina": ["Peru", "Brazil"],

        "Brazil": ["Argentina", "Peru", "Venezuela", "North Africa"],

        "Venezuela": ["Central America", "Peru", "Brazil"],

        "Peru": ["Venezuela", "Brazil", "Argentina"],

        "Congo": ["East Africa", "North Africa", "South Africa"],

        "East Africa": ["Madagascar", "South Africa", "Congo", "North Africa", "Egypt", "Middle East"],

        "Egypt": ["North Africa", "East Africa", "Middle East", "Southern Europe"],

        "Madagascar": ["South Africa", "East Africa"],

        "North Africa": ["Brazil", "Western Europe", "Southern Europe", "Egypt", "East Africa", "Congo"],

        "South Africa": ["Congo", "East Africa", "Madagascar"],

        "Eastern Australia": ["Western Australia", "New Guinea"],

        "New Guinea": ["Eastern Australia", "Western Australia", "Indonesia"],

        "Indonesia": ["Siam", "New Guinea", "Western Australia"],

        "Western Australia": ["Eastern Australia", "New Guinea", "Indonesia"],

        "Afghanistan": ["Ukraine", "Ural", "China", "India", "Middle East"],

        "China": ["Siam", "India", "Afghanistan", "Ural", "Mongolia", "Siberia"],

        "India": ["Middle East", "Afghanistan", "China", "Siam"],

        "Irkutsk": ["Mongolia", "Kamchatka", "Yakutsk", "Siberia"],

        "Japan": ["Mongolia", "Kamchatka"], "Kamchatka": ["Japan", "Mongolia", "Irkutsk", "Yakutsk", "Alaska"],

        "Middle East": ["East Africa", "Egypt", "Southern Europe", "Ukraine", "Afghanistan", "India"],

        "Mongolia": ["China", "Siberia", "Irkutsk", "Kamchatka", "Japan"],

        "Siam": ["India", "China", "Indonesia"],

        "Siberia": ["Ural", "China", "Mongolia", "Irkutsk", "Yakutsk"],

        "Ural": ["Ukraine", "Afghanistan", "China", "Siberia"],

        "Yakutsk": ["Siberia", "Irkutsk", "Kamchatka"],

        "Great Britain": ["Iceland", "Scandinavia", "Northern Europe", "Western Europe"],

        "Iceland": ["Greenland", "Great Britain", "Scandinavia"],

        "Northern Europe": ["Southern Europe", "Western Europe", "Great Britain", "Scandinavia", "Ukraine"],

        "Scandinavia": ["Ukraine", "Northern Europe", "Iceland", "Great Britain"],

        "Southern Europe": ["North Africa", "Egypt", "Middle East", "Ukraine", "Northern Europe", "Western Europe"],

        "Ukraine": ["Ural", "Afghanistan", "Middle East", "Southern Europe", "Northern Europe", "Scandinavia"],

        "Western Europe": ["North Africa", "Southern Europe", "Northern Europe", "Great Britain"]
    }
    return dictionary


class Continent:
    def __init__(self, name):
        """
        Initializes a Continent object with a given name
        :param name: The name of the continent
        """
        self.continent_name = name
        self.countries_in_continent = []

    def add_country(self, country):
        """
        Adds a country to the continent
        :param country: The name of the country to be added.
        :return: [NONE]
        """
        self.countries_in_continent.append(country)

    def get_bonus(self):
        """
        Retrieves the bonus value associated with the continent.
        :return: The bonus value for controlling the entire continent 'bonuses[self.continent_name]'
        """
        bonuses = {
            "North America": 6,
            "South America": 2,
            "Africa": 3,
            "Australia": 2,
            "Asia": 7,
            "Europe": 5,
        }
        return bonuses[self.continent_name]


def create_continents():
    """
    Creates and initializes Continent objects
    :return: A list of Continent objects 'continents'
    """
    continents = [
        Continent("North America"),
        Continent("South America"),
        Continent("Africa"),
        Continent("Australia"),
        Continent("Asia"),
        Continent("Europe"),
    ]
    index = 0
    neighbour_dict = create_neighbours()
    for k, v in neighbour_dict.items():
        if index < 9:
            continents[0].add_country(k)
        elif index < 13:
            continents[1].add_country(k)
        elif index < 19:
            continents[2].add_country(k)
        elif index < 23:
            continents[3].add_country(k)
        elif index < 35:
            continents[4].add_country(k)
        else:
            continents[5].add_country(k)
        index += 1
    return continents
