import pygame
from button import Button
from countries import Country
from main_menu import MainMenu
from player import Human
import threading
import os

pygame.init()

plate_img = pygame.image.load("images\\dice_table.png")
map_img = pygame.image.load("images\\map.jpg")
button_image = pygame.image.load("images\\button_high.png")
button_hover_image = pygame.image.load("images\\button_hover.png")
font1 = "fonts\\font1.ttf"
# Color sets
YELLOW = (201, 227, 32)
PINK = (201, 171, 198)
BROWN = (181, 138, 72)
GREEN = (84, 199, 153)
RED = (204, 40, 37)
BLUE = (47, 122, 250)


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.players = 0
        self.AI_players = 0
        self.center_x, self.center_y = screen.get_width() / 2, screen.get_height() / 2
        self.map_img = pygame.transform.scale(map_img, (screen.get_width(), screen.get_height()))
        self.plate_img = pygame.transform.scale(plate_img, (int(screen.get_height() / 4), int(screen.get_height() / 4)))
        self.state = None
        self.buttons = self.create_buttons()
        self.countries = []
        self.player_profiles = []
        self.COLORS = [YELLOW, PINK, BROWN, GREEN, RED, BLUE]
        self.COLORS_STR = ["Yellow", "Pink", "Brown", "Green", "Red", "Blue"]
        self.current_turn = 0
        self.turn_indicator = self.create_turn_indicator()
        self.lock = threading.Lock()

    # Draws all necessary elements on the map
    def draw(self):
        self.screen.blit(self.map_img, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)
        if self.countries:
            for country in self.countries:
                country.draw()
        for player in self.player_profiles:
            player.draw_profile()
        self.draw_dice_plate()
        self.draw_turn_indicator()

    # checks clicks on buttons and countries
    def check_clicks(self, event):
        for button in self.buttons:
            button.check_click(event)

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    # Sets number of human and ai players
    def set_players_and_ai(self, players, ai):
        self.players = players
        self.AI_players = ai

    # Creates all necessary buttons for gameplay
    # So far just back button
    def create_buttons(self):
        buttons = []
        back = Button(button_image, button_hover_image, (0, 0), "Back",
                      int(self.center_y * 0.08), int(self.center_x * 0.1), int(self.center_y * 0.1), font=font1,
                      action=lambda: self.set_state(0))
        buttons.append(back)
        return buttons

    # Creates players
    # So far creates only Human Players, will be changed when we implement AI
    def create_players(self):
        all_profiles = MainMenu.player_images
        players_in_game = []
        for i in range(self.players + self.AI_players):
            players_in_game.append(Human(self.screen, all_profiles[i], self.COLORS[i], self.COLORS_STR[i]))
        for i, player in enumerate(players_in_game):
            width = int(self.center_x * 0.08)
            height = width
            player.set_pos_size(self.screen.get_width() - width,
                                int(self.screen.get_height() / 10 * (i+1)),
                                width, height)
        self.player_profiles = players_in_game

    # Returns a list of Player objects
    def get_players(self):
        return self.player_profiles

    # Another dummy thing, just to see who's turn it is right now
    # We gonna think about something better than green triangle
    def create_turn_indicator(self):
        size = self.center_y * 0.1
        turn_indicator = pygame.image.load("images\\green_tri.png")
        turn_indicator = pygame.transform.scale(turn_indicator, (size, size))
        return turn_indicator

    # Same as above
    def draw_turn_indicator(self):
        x = self.player_profiles[0].pos[0] - self.turn_indicator.get_width()
        y = self.player_profiles[self.current_turn].pos[1]
        self.screen.blit(self.turn_indicator, (x, y))

    def draw_dice_plate(self):
        self.screen.blit(self.plate_img, (self.screen.get_width() - self.plate_img.get_width(),
                                          self.screen.get_height() - self.plate_img.get_height()))

    # Keeps track of player turn here to indicate their turn somehow, for now it's just green triangle
    def change_turn(self, turn):
        self.current_turn = turn

    def load_country_image(self, image_path):
        # Load the image and create a Country object
        cleaned_name = image_path.replace("country_imgs\\", "").replace(".png", "")
        country = Country(self.screen, pygame.image.load(image_path).convert_alpha(), cleaned_name)
        with self.lock:  # Ensure thread-safe append
            self.countries.append(country)

    def load_all_images(self):
        folder_path = "country_imgs"
        images = os.listdir(folder_path)
        for file in images:
            self.load_country_image(os.path.join(folder_path, file))

    def create_countries(self):
        # Start a single thread to load all images
        threading.Thread(target=self.load_all_images).start()
