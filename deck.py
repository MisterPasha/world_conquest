import pygame
import random
from main_menu import draw_text

pygame.init()

infantry_image = pygame.image.load("images\\infantry.jpg")
cavalry_image = pygame.image.load("images\\cavalry.png")
artillery_image = pygame.image.load("images\\artillery.jpg")
card_image = pygame.image.load("images\\card.png")


class Deck:
    def __init__(self, screen):
        self.screen = screen
        self.cards = []

    def create_cards(self, map_):
        width = int(self.screen.get_height() * 0.07)
        infantry = pygame.transform.scale(infantry_image, (width, width))
        cavalry = pygame.transform.scale(cavalry_image, (width, width))
        artillery = pygame.transform.scale(artillery_image, (width, width))
        units = ["Infantry"] * 14 + ["Cavalry"] * 14 + ["Artillery"] * 14
        for country, unit in zip(map_.countries, units):
            if unit == "Infantry":
                self.cards.append(Card(self.screen, country.get_name(), unit, infantry))
            elif unit == "Cavalry":
                self.cards.append(Card(self.screen, country.get_name(), unit, cavalry))
            if unit == "Artillery":
                self.cards.append(Card(self.screen, country.get_name(), unit, artillery))

    def get_card(self):
        index = random.randint(0, len(self.cards) - 1)
        card = self.cards.pop(index)
        return card


class Card:
    def __init__(self, screen, country_name, army_type, img):
        self.screen = screen
        self.country_name = country_name
        self.army_type = army_type
        self.army_type_image = img
        self.width = int(self.screen.get_width() * 0.065)
        self.height = int(self.screen.get_height() * 0.17)
        self.card = pygame.transform.scale(card_image, (self.width, self.height))

    def draw(self, x, y):
        self.screen.blit(self.card, (x, y))
        draw_text(self.screen, self.country_name, 16, (0, 0, 0), x + 15, y + 15)
        self.screen.blit(self.army_type_image, (x + 15, y + 40))

