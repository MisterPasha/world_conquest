import pygame
from button import Button
from countries import Country
from main_menu import MainMenu
from player import Human
from player import Player
import random

pygame.init()

map_img = pygame.image.load("images\\map1.jpg")
button_image = pygame.image.load("images\\button_high.png")
button_hover_image = pygame.image.load("images\\button_hover.png")
font1 = "fonts\\font1.ttf"


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.players = 0
        self.AI_players = 0
        self.center_x, self.center_y = screen.get_width() / 2, screen.get_height() / 2
        self.map_img = pygame.transform.scale(map_img, (screen.get_width(), screen.get_height()))
        self.state = None
        self.buttons = self.create_buttons()
        self.countries = self.create_countries()
        self.player_profiles = None

    def draw(self):
        self.screen.blit(self.map_img, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)
        for country in self.countries:
            country.draw()
        for player in self.player_profiles:
            player.draw_profile()

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def set_players_and_ai(self, players, ai):
        self.players = players
        self.AI_players = ai

    def check_clicks(self, event):
        for button in self.buttons:
            button.check_click(event)

    def change_color(self):
        colors = ["red", "blue", "brown", "yellow", "pink", "gray"]
        for country in self.countries:
            country.change_color(random.choice(colors))

    def create_buttons(self):
        buttons = []
        back = Button(button_image, button_hover_image, (0, 0), "Back",
                      int(self.center_y * 0.08), int(self.center_x * 0.1), int(self.center_y * 0.1), font=font1,
                      action=lambda: self.set_state(0))
        change_color = Button(button_image, button_hover_image, (self.center_x, self.center_y ), "Change",
                      int(self.center_y * 0.1), int(self.center_x * 0.2), int(self.center_y * 0.2), font=font1,
                      action=lambda: self.change_color())
        buttons.append(back)
        buttons.append(change_color)
        return buttons

    def create_players(self):
        all_profiles = MainMenu.player_images
        players_in_game = []
        colors = ["yellow", "pink", "brown", "gray", "red", "blue"]
        for i in range(self.players + self.AI_players):
            players_in_game.append(Player(self.screen, all_profiles[i], colors[i]))
        for i, player in enumerate(players_in_game):
            width = int(self.center_x * 0.1)
            height = width
            player.set_pos_size(self.screen.get_width() - width,
                                int(self.screen.get_height() / 8 * (i+1)),
                                width, height)
        self.player_profiles = players_in_game

    def create_countries(self):
        country1 = pygame.image.load("countries\\country1.png").convert_alpha()
        country2 = pygame.image.load("countries\\country2.png").convert_alpha()
        country3 = pygame.image.load("countries\\country3.png").convert_alpha()
        country4 = pygame.image.load("countries\\country4.png").convert_alpha()
        country5 = pygame.image.load("countries\\country5.png").convert_alpha()
        country6 = pygame.image.load("countries\\country6.png").convert_alpha()
        country7 = pygame.image.load("countries\\country7.png").convert_alpha()
        country8 = pygame.image.load("countries\\country8.png").convert_alpha()
        country9 = pygame.image.load("countries\\country9.png").convert_alpha()
        country1 = Country(self.screen, country1)
        country2 = Country(self.screen, country2)
        country3 = Country(self.screen, country3)
        country4 = Country(self.screen, country4)
        country5 = Country(self.screen, country5)
        country6 = Country(self.screen, country6)
        country7 = Country(self.screen, country7)
        country8 = Country(self.screen, country8)
        country9 = Country(self.screen, country9)
        return [country1, country2, country3, country4, country5, country6, country7, country8, country9]
