import pygame
from main_menu import MainMenu
from map import Map

pygame.init()


class Game:
    # Game States
    EXIT = -1
    MAIN_MENU = 0
    GAMEPLAY_1 = 1  # 3-6 players game
    GAMEPLAY_2 = 2  # 2 players game
    GAME_OVER = 3

    def __init__(self, screen, clock, window_size):
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.running = True
        # set initial state
        self.game_state = self.MAIN_MENU
        # List of Player objects
        self.players = None
        # Current player
        self.current_turn = 0
        # initialise MainMenu object
        self.main_menu = MainMenu(self.screen)
        # initialise Map object
        self.map = Map(self.screen)

    # Main running loop
    def run(self):
        while self.running:
            self.events()
            self.draw()
            self.clock.tick(60)
            pygame.display.flip()

    # Controls all event types
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.game_state == self.MAIN_MENU:
                self.main_menu.check_clicks(event)
            elif self.game_state == self.GAMEPLAY_1:
                self.map.check_clicks(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_country_clicks(event.pos)
            elif self.game_state == self.GAMEPLAY_2:
                continue
            elif self.game_state == self.EXIT:
                self.running = False

    # Draws all elements on the screen
    def draw(self):
        if self.game_state == self.MAIN_MENU:
            self.check_state_main_menu()
            self.main_menu.draw()
        if self.game_state == self.GAMEPLAY_1:
            self.check_state_gameplay()
            self.map.draw()

    # Keeps track of current game states in objects and activates necessary functions during MAIN MENU state
    def check_state_main_menu(self):
        if self.main_menu.get_state() == self.MAIN_MENU:
            self.game_state = self.MAIN_MENU
        elif self.main_menu.get_state() == self.GAMEPLAY_1:
            self.map.set_state(self.GAMEPLAY_1)
            # When decision on number of players has been done it passes it to Map
            self.map.set_players_and_ai(self.main_menu.get_num_players(), self.main_menu.get_num_ai_players())
            self.map.create_players()
            # Define players
            self.players = self.map.get_players()
            self.game_state = self.GAMEPLAY_1
        elif self.main_menu.get_state() == self.GAMEPLAY_2:
            self.game_state = self.GAMEPLAY_2
            self.map.set_state(self.GAMEPLAY_2)
        elif self.main_menu.get_state() == self.EXIT:
            self.game_state = self.EXIT

    # Keeps track of current game states in objects and activates necessary functions during GAMEPLAY1 state
    def check_state_gameplay(self):
        if self.map.get_state() == self.MAIN_MENU:
            self.game_state = self.MAIN_MENU
            self.main_menu.change_state(self.game_state)
        elif self.game_state == self.GAMEPLAY_1:
            pass

    def pass_turn(self):
        if self.current_turn == len(self.players) - 1:
            self.current_turn = 0
        else:
            self.current_turn += 1
        self.map.change_turn(self.current_turn)

    def occupy_country(self, country):
        current_player = self.players[self.current_turn]
        if country.owner is None:
            country.set_owner(current_player)
            country.set_color()
            country.add_troop()
            self.pass_turn()
        elif country.owner is not current_player:
            print("You are doing something naughty!")
        else:
            country.add_troop()
            self.pass_turn()
        print(country.owner)

    def handle_country_clicks(self, mouse_pos):
        for country in self.map.countries:
            if country.country_btn.rect.collidepoint(mouse_pos):
                self.occupy_country(country)
