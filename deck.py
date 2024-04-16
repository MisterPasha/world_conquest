import pygame  # Import the pygame library for game development
import random  # RNG
from main_menu import draw_text, draw_text2  # Import draw_text class from main_menu
from itertools import (
    zip_longest,
)  # Import zip_longest for handling iterators of unequal length
import os  # provides functions for interacting with the operating system

# Initialize pygame
pygame.init()

# Load images
infantry_image = pygame.image.load("images\\infantry.png")
cavalry_image = pygame.image.load("images\\cavalry.png")
artillery_image = pygame.image.load("images\\artillery.png")
card_image = pygame.image.load("images\\empty_card.png")

mission_cards_ = [
    pygame.image.load("mission_cards\\task1.png"),
    pygame.image.load("mission_cards\\task2.png"),
    pygame.image.load("mission_cards\\task3.png"),
    pygame.image.load("mission_cards\\task4.png"),
    pygame.image.load("mission_cards\\task5.png"),
    pygame.image.load("mission_cards\\task6.png"),
    pygame.image.load("mission_cards\\task7.png"),
    pygame.image.load("mission_cards\\task8.png"),
]


class Deck:
    def __init__(self, screen):
        """
        Initialize a Deck object
        :param screen: The Pygame screen surface
        """
        self.screen = screen
        self.cards = []

    def create_cards(self, map_):
        """
        Creates cards for each country on the map with corresponding units and images
        :param map_: map object (with the country >.>)
        :return: [NONE]
        """
        card_images = self.load_card_images()
        width = int(self.screen.get_height() * 0.05)
        infantry = pygame.transform.scale(infantry_image, (width, width))
        cavalry = pygame.transform.scale(cavalry_image, (width, width))
        artillery = pygame.transform.scale(artillery_image, (width, width))
        units = ["Infantry"] * 14 + ["Cavalry"] * 14 + ["Artillery"] * 14 + ["Wild"] * 2
        for country, unit, card_img in zip_longest(map_.countries, units, card_images):
            if unit == "Infantry":
                self.cards.append(Card(self.screen, card_img, country.get_name(), unit, infantry))
            elif unit == "Cavalry":
                self.cards.append(Card(self.screen, card_img, country.get_name(), unit, cavalry))
            elif unit == "Artillery":
                self.cards.append(
                    Card(self.screen, card_img, country.get_name(), unit, artillery)
                )
            elif unit == "Wild":
                self.cards.append(Card(self.screen, card_image, None, unit, None))

    def load_card_images(self):
        """
        Loads card images from the 'card_images' folder
        :return: 'images' (loaded cards)
        """
        folder = "card_images"
        images = []
        for filename in os.listdir(folder):
            img = pygame.image.load(os.path.join(folder, filename))
            if img is not None:
                images.append(img)
        return images

    def get_card(self):
        """
        Get a random card from the deck
        :return: card
        """
        index = random.randint(0, len(self.cards) - 1)
        card = self.cards.pop(index)
        return card


class Card:
    def __init__(self, screen, card_img, country_name, army_type, img):
        """
        Initialize a Card object

        :param screen: The Pygame screen surface
        :param country_name: The name of the country associated with the card
        :param army_type: The type of army associated with the card. (e.g., Infantry, Cavalry, Artillery)
        :param img: The image representing the army type
        """
        self.screen = screen
        self.country_name = country_name
        self.army_type = army_type
        self.army_type_image = img
        self.width = int(self.screen.get_width() * 0.07)
        self.height = int(self.screen.get_height() * 0.19)
        self.card = pygame.transform.scale(card_img, (self.width, self.height))
        icon_width = int(self.width * 0.4)
        self.infantry = pygame.transform.scale(infantry_image, (icon_width, icon_width))
        self.cavalry = pygame.transform.scale(cavalry_image, (icon_width, icon_width))
        self.artillery = pygame.transform.scale(
            artillery_image, (icon_width, icon_width)
        )

    def draw(self, x, y):
        """
        Draw the card on the screen
        :param x: The x-coordinate
        :param y: The y-coordinate
        :return: [NONE]
        """
        if self.army_type == "Wild":
            self.screen.blit(self.card, (x, y))
            self.screen.blit(
                self.infantry, (x + int(self.width * 0.3), y + int(self.height * 0.1))
            )
            self.screen.blit(
                self.artillery, (x + int(self.width * 0.3), y + int(self.height * 0.4))
            )
            self.screen.blit(
                self.cavalry, (x + int(self.width * 0.3), y + int(self.height * 0.7))
            )
        else:
            self.screen.blit(self.card, (x, y))
            draw_text2(
                self.screen,
                self.country_name,
                int(self.height * 0.13),
                (0, 0, 0),
                x + int(self.width * 0.18),
                y + int(self.width * 0.07),
            )
            self.screen.blit(
                self.army_type_image,
                (x + int(self.width * 0.27), y + int(self.height * 0.65)),
            )


class MissionCards:
    def __init__(self, screen):
        """
        Initializes MissionCards object
        :param screen: The pygame screen to draw the mission cards on
        """
        self.screen = screen
        self.width = int(self.screen.get_width() * 0.08)
        self.height = int(self.screen.get_height() * 0.22)
        self.mission_cards = [
            pygame.transform.scale(card, (self.width, self.height))
            for card in mission_cards_
        ]

    def draw(self, id_, x, y, player_to_destroy=None):
        """
        Draws a mission card on the screen
        :param id_: The id of the mission card to draw
        :param x: The x-coordinate where the mission card will be drawn
        :param y: The y-coordinate where the mission card will be drawn
        :param player_to_destroy: The player whose armies need to be destroyed for the mission
        :return: [NONE]
        """
        self.screen.blit(self.mission_cards[id_ - 1], (x, y))
        if id_ == 7:
            draw_text(
                self.screen,
                player_to_destroy,
                18,
                (0, 0, 0),
                x + int(self.width * 0.2),
                y + int(self.height * 0.8),
            )

    def mission_completed(self, mission_id, player):
        """
        Checks if a player has completed a mission
        :param mission_id:
        :param player: The player object whose completion status is to be checked.
        :return: 'True' if the player has completed the mission, 'False' otherwise.
        """
        player_continents = [
            continent.continent_name for continent in player.continents
        ]

        # Capture Europe, Australia and one other continent
        def mission1(player_):
            """
            Checks if a player has completed a mission 1
            :return: 'True' if the player has completed the mission, 'False' otherwise.
            """
            if (
                    "Europe" in player_continents
                    and "Australia" in player_continents
                    and len(player_continents) >= 3
            ):
                return True
            return False

        # Capture Europe, South America and one other continent
        def mission2(player_):
            """
            Checks if a player has completed a mission 2
            :return: 'True' if the player has completed the mission, 'False' otherwise.
            """
            if (
                    "Europe" in player_continents
                    and "South America" in player_continents
                    and len(player_continents) >= 3
            ):
                return True
            return False

        # Capture North America and Africa
        def mission3(player_):
            """
            Checks if a player has completed a mission 3
            :return: 'True' if the player has completed the mission, 'False' otherwise.
            """
            if "North America" in player_continents and "Africa" in player_continents:
                return True
            return False

        # Capture Asia and South America
        def mission4(player_):
            """
            Checks if a player has completed a mission 4
            :return: 'True' if the player has completed the mission, 'False' otherwise.
            """
            if "Asia" in player_continents and "South America" in player_continents:
                return True
            return False

        # Capture North America and Australia
        def mission5(player_):
            """
            Checks if a player has completed a mission 5
            :return: 'True' if the player has completed the mission, 'False' otherwise.
            """
            if (
                    "North America" in player_continents
                    and "Australia" in player_continents
            ):
                return True
            return False

        # Capture 24 territories
        def mission6(player_):
            """
            Checks if a player has completed a mission 6
            :return: 'True' if the player has completed the mission, 'False' otherwise.
            """
            if len(player_.countries) >= 24:
                return True
            return False

        # Destroy all armies of a named opponent or, in case being the named player oneself -
        # Capture 24 countries
        def mission7(player_):
            """
            Checks if a player has completed a mission 7
            :return: 'True' if the player has completed the mission, 'False' otherwise.
            """
            if player_.player_to_destroy == player_:
                if len(player_.countries) >= 24:
                    return True
            else:
                if not player_.player_to_destroy.playing:
                    return True
            return False

        # Capture 18 territories and occupy each with 2 troops
        def mission8(player_):
            """
            Checks if a player has completed a mission 8
            :return: 'True' if the player has completed the mission, 'False' otherwise.
            """
            counter = 0
            for country in player_.countries:
                if country.troops >= 2:
                    counter += 1
            if counter >= 18:
                return True
            return False

        mission_dict = {
            1: mission1,
            2: mission2,
            3: mission3,
            4: mission4,
            5: mission5,
            6: mission6,
            7: mission7,
            8: mission8,
        }

        return mission_dict[mission_id](player)

# Finished
