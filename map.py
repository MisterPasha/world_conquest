import pygame  # Import the pygame library for game development
from button import Button  # Importing Button class
from countries import Country
from main_menu import MainMenu
from player import Human
import threading
import os

pygame.init()

# ...
plate_img = pygame.image.load("images\\dice_table.png")
map_img = pygame.image.load("images\\map.png")
ports_img = pygame.image.load("images\\ports.png")
sea_paths_img = pygame.image.load("images\\sea_paths.png")

button_image = pygame.image.load("images\\button_high.png")
button_hover_image = pygame.image.load("images\\button_hover.png")
font1 = "fonts\\font1.ttf"

# Color sets
YELLOW = (206, 222, 100)
PINK = (201, 171, 198)
BROWN = (184, 149, 95)
GREEN = (84, 199, 153)
RED = (168, 69, 67)
BLUE = (57, 108, 196)


class Map:
    def __init__(self, screen):
        """

        :param screen:
        """
        self.screen = screen
        self.players = 0
        self.AI_players = 0
        self.center_x, self.center_y = screen.get_width() / 2, screen.get_height() / 2

        self.map_img = pygame.transform.scale(
            map_img, (screen.get_width(), screen.get_height())
        )
        self.plate_img = pygame.transform.scale(
            plate_img, (int(screen.get_height() / 4.5), int(screen.get_height() / 4.5))
        )
        self.ports_img = pygame.transform.scale(
            ports_img, (screen.get_width(), screen.get_height())
        )
        self.sea_paths_img = pygame.transform.scale(
            sea_paths_img, (screen.get_width(), screen.get_height())
        )
        self.state = None
        self.buttons = self.create_buttons()
        self.countries = []
        self.neighbours = self.create_neighbours()
        self.player_profiles = []
        self.COLORS = [YELLOW, PINK, BROWN, GREEN, RED, BLUE]
        self.COLORS_STR = ["Yellow", "Pink", "Brown", "Green", "Red", "Blue"]
        self.current_turn = 0
        self.turn_indicator = self.create_turn_indicator()
        self.lock = threading.Lock()

    def draw(self):
        """
        Draws all necessary elements on the map
        :return:
        """
        self.screen.blit(self.map_img, (0, 0))
        self.screen.blit(self.sea_paths_img, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)
        if self.countries:
            for country in self.countries:
                country.draw()
        self.screen.blit(self.ports_img, (0, 0))
        for player in self.player_profiles:
            player.draw_profile()
        self.draw_dice_plate()
        self.draw_turn_indicator()

    def check_clicks(self, event):
        """
        Checks clicks on buttons and countries
        :param event:
        :return:
        """
        for button in self.buttons:
            button.check_click(event)

    def drop_highlights(self):
        for c in self.countries:
            c.highlighted = False

    def get_state(self):
        """

        :return: self.state
        """
        return self.state

    def set_state(self, new_state):
        """

        :param new_state:
        :return:
        """
        self.state = new_state

    # Sets number of human and AI players
    def set_players_and_ai(self, players, ai):
        """

        :param players:
        :param ai:
        :return:
        """
        self.players = players
        self.AI_players = ai

    def create_buttons(self):
        """
        Creates all necessary buttons for gameplay.
        So far just back button
        :return: buttons
        """
        buttons = []
        back = Button(
            button_image,
            button_hover_image,
            (0, 0),
            "Back",
            int(self.center_y * 0.08),
            int(self.center_x * 0.1),
            int(self.center_y * 0.1),
            font=font1,
            action=lambda: self.set_state(0)
        )
        buttons.append(back)
        return buttons

    def create_players(self):
        """
        Creates players.
        So far creates only Human Players, will be changed when we implement AI
        :return:
        """
        all_profiles = MainMenu.player_images
        players_in_game = []
        for i in range(self.players + self.AI_players):
            players_in_game.append(
                Human(self.screen, all_profiles[i], self.COLORS[i], self.COLORS_STR[i])
            )
        for i, player in enumerate(players_in_game):
            width = int(self.center_x * 0.08)
            height = width
            player.set_pos_size(
                self.screen.get_width() - width,
                int(self.screen.get_height() / 10 * (i + 1)),
                width,
                height,
            )
        self.player_profiles = players_in_game

    def get_players(self):
        """
        Returns a list of Player objects
        :return: self.player_profiles
        """
        return self.player_profiles

    def create_turn_indicator(self):
        """
        Another dummy thing, just to see who's turn it is right now.
        Were going to think about something better than green triangle
        :return: turn_indicator
        """
        size = self.center_y * 0.05
        turn_indicator = pygame.image.load("images\\green_dot.png")
        turn_indicator = pygame.transform.scale(turn_indicator, (size, size))
        return turn_indicator

    # Same as above
    def draw_turn_indicator(self):
        """

        :return:
        """
        x = self.player_profiles[0].pos[0] - self.turn_indicator.get_width()
        y = self.player_profiles[self.current_turn].pos[1]
        self.screen.blit(self.turn_indicator, (x, y))

    def draw_dice_plate(self):
        """

        :return:
        """
        self.screen.blit(
            self.plate_img,
            (
                self.screen.get_width() - self.plate_img.get_width(),
                self.screen.get_height() - self.plate_img.get_height(),
            ),
        )

    def all_countries_have_owner(self):
        for country in self.countries:
            if country.owner is None:
                return False
        return True

    def change_turn(self, turn):
        """
        Keeps track of player turn here to indicate their turn somehow, for now it's just green triangle
        :param turn:
        :return:
        """
        self.current_turn = turn

    def load_country_image(self, image_path):
        """

        :param image_path:
        :return:
        """
        # Load the image and create a Country object
        cleaned_name = image_path.replace("country_imgs\\", "").replace(".png", "")
        country = Country(
            self.screen, pygame.image.load(image_path).convert_alpha(), cleaned_name
        )
        with self.lock:  # Ensure thread-safe append
            self.countries.append(country)

    def load_all_images(self):
        """

        :return:
        """
        folder_path = "country_imgs"
        images = os.listdir(folder_path)
        for file in images:
            self.load_country_image(os.path.join(folder_path, file))

    def create_countries(self):
        """
        Start a single thread to load all images
        :return:
        """
        threading.Thread(target=self.load_all_images).start()

    def get_neighbours(self, country_name):
        """

        :param country_name:
        :return: self.neighbours[country_name]
        """
        return self.neighbours[country_name]

    def get_neighbours_countries(self, country):
        country_name = country.get_name()
        neighbour_country_names = self.get_neighbours(country_name)
        countries = []
        for c in self.countries:
            if c.get_name() in neighbour_country_names:
                countries.append(c)
        return countries

    def create_neighbours(self):
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
