import pygame  # Import the pygame library for game development
import random  # RNG
from main_menu import draw_text  # Import draw_text class from main_menu
from itertools import zip_longest

# Initialize pygame
pygame.init()

# Load images
infantry_image = pygame.image.load("images\\infantry.jpg")
cavalry_image = pygame.image.load("images\\cavalry.png")
artillery_image = pygame.image.load("images\\artillery.jpg")
card_image = pygame.image.load("images\\card.png")


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
        Create cards for the deck based on the provided map
        :param map_: The map object containing countries
        :return: [NONE]
        """
        width = int(self.screen.get_height() * 0.07)
        infantry = pygame.transform.scale(infantry_image, (width, width))
        cavalry = pygame.transform.scale(cavalry_image, (width, width))
        artillery = pygame.transform.scale(artillery_image, (width, width))
        units = ["Infantry"] * 14 + ["Cavalry"] * 14 + ["Artillery"] * 14 + ["Wild"] * 14
        for country, unit in zip(map_.countries, units):
            if unit == "Infantry":
                self.cards.append(Card(self.screen, country.get_name(), unit, infantry))
            elif unit == "Cavalry":
                self.cards.append(Card(self.screen, country.get_name(), unit, cavalry))
            elif unit == "Artillery":
                self.cards.append(
                    Card(self.screen, country.get_name(), unit, artillery)
                )
            elif unit == "Wild":
                self.cards.append(Card(self.screen, None, None, None))

    def get_card(self):
        """
        Get a random card from the deck
        :return: card
        """
        index = random.randint(0, len(self.cards) - 1)
        card = self.cards.pop(index)
        return card


class Card:
    def __init__(self, screen, country_name, army_type, img):
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
        self.width = int(self.screen.get_width() * 0.065)
        self.height = int(self.screen.get_height() * 0.17)
        self.card = pygame.transform.scale(card_image, (self.width, self.height))
        icon_width = int(self.width * 0.6)
        self.infantry = pygame.transform.scale(infantry_image, (icon_width, icon_width))
        self.cavalry = pygame.transform.scale(cavalry_image, (icon_width, icon_width))
        self.artillery = pygame.transform.scale(artillery_image, (icon_width, icon_width))

    def draw(self, x, y):
        """
        Draw the card on the screen
        :param x: The x-coordinate
        :param y: The y-coordinate
        :return: [NONE]
        """
        if self.army_type == "Wild":
            self.screen.blit(self.card, (x, y))
            self.screen.blit(self.infantry, (x + int(self.width * 0.2), y + int(self.height * 0.1)))
            self.screen.blit(self.artillery, (x + int(self.width * 0.2), y + int(self.height * 0.4)))
            self.screen.blit(self.cavalry, (x + int(self.width * 0.2), y + int(self.height * 0.7)))
        else:
            self.screen.blit(self.card, (x, y))
            draw_text(self.screen, self.country_name, 16, (0, 0, 0), x + int(self.width * 0.2), y + int(self.width * 0.2))
            self.screen.blit(self.army_type_image, (x + int(self.width * 0.2), y + int(self.height * 0.5)))
