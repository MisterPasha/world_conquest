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

    def __init__(self, screen, clock, window_size):
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.running = True
        # set initial state
        self.game_state = self.MAIN_MENU
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
            self.game_state = self.GAMEPLAY_1
            self.map.set_state(self.GAMEPLAY_1)
            # When decision on number of players has been done it passes it to Map
            self.map.set_players_and_ai(self.main_menu.get_num_players(), self.main_menu.get_num_ai_players())
            self.map.create_players()
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

