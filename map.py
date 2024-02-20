import pygame
from button import Button
from countries import Country
import random

pygame.init()

map_img = pygame.image.load("images\\map1.jpg")
button_image = pygame.image.load("images\\button_high.png")
button_hover_image = pygame.image.load("images\\button_hover.png")
font1 = "fonts\\font1.ttf"


class Map:
    def __init__(self, screen, players, ais):
        self.screen = screen
        self.players = players
        self.AI_players = ais
        self.center_x, self.center_y = screen.get_width() / 2, screen.get_height() / 2
        self.map_img = pygame.transform.scale(map_img, (screen.get_width(), screen.get_height()))
        self.state = None
        self.buttons = self.create_buttons()
        self.countries = self.create_countries()

    def draw(self):
        self.screen.blit(self.map_img, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)
        for country in self.countries:
            country.draw()

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def check_clicks(self, event):
        for button in self.buttons:
            button.check_click(event)

    def change_color(self):
        colors = ["red", "blue", "green", "yellow", "pink", "white"]
        for country in self.countries:
            country.change_color(random.choice(colors))

    def create_buttons(self):
        buttons = []
        back = Button(button_image, button_hover_image, (0, 0), "Back",
                      int(self.center_y * 0.08), int(self.center_x * 0.1), int(self.center_y * 0.1), font=font1,
                      action=lambda: self.set_state(0))
        change_color = Button(button_image, button_hover_image, (self.center_x,self.center_y ), "Change",
                      int(self.center_y * 0.1), int(self.center_x * 0.2), int(self.center_y * 0.2), font=font1,
                      action=lambda: self.change_color())
        buttons.append(back)
        buttons.append(change_color)
        return buttons

    def create_countries(self):
        country_image = pygame.image.load("images\\country1.png").convert_alpha()
        country1 = Country(self.screen, country_image)
        return [country1]
