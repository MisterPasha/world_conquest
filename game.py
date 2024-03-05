import pygame
import random
from main_menu import MainMenu
from map import Map
from dice import Dice

pygame.init()

class Game:
    paper_img = pygame.image.load("images\\gameplay_paper.png")

    # Game States
    EXIT = -1
    MAIN_MENU = 0
    GAMEPLAY_1 = 1  # 3-6 players game
    GAMEPLAY_2 = 2  # 2 players game
    GAME_OVER = 3

    # Gameplay stages
    CHOOSE_FIRST_TURN = 0
    SETUP = 1
    DRAFT = 2
    ATTACK = 3
    FORTIFY = 4

    def __init__(self, screen, clock, window_size):
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.running = True
        # image paper in gameplay
        self.paper_img = pygame.transform.scale(self.paper_img, (screen.get_width(), screen.get_height()))
        # set initial state
        self.game_state = self.MAIN_MENU
        # set initial gameplay stage
        self.gameplay_stage = self.CHOOSE_FIRST_TURN
        # List of Player objects
        self.players = None
        # Current player
        self.current_turn = 0
        # initialise MainMenu object
        self.main_menu = MainMenu(self.screen)
        # initialise Map object
        self.map = None
        self.countries_divided = False
        # All necessary dice attributes
        self.dice = Dice(self.screen)
        self.showing_dice_animation = False
        self.animation_start_time = None
        self.dice_thrown = []
        self.dice_throw_index = 0

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
                self.map.check_clicks(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_country_clicks(event.pos)
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
            if self.gameplay_stage == self.CHOOSE_FIRST_TURN:
                self.screen.blit(self.paper_img, (0, 0))
            self.dice_animate()
        if self.game_state == self.GAMEPLAY_2:
            self.check_state_gameplay()
            self.map.draw()
            if self.gameplay_stage == self.CHOOSE_FIRST_TURN:
                self.screen.blit(self.paper_img, (0, 0))
            self.dice_animate()

    # Keeps track of current game states in objects and activates necessary functions
    # (for gameplay setup) during MAIN MENU state
    def check_state_main_menu(self):
        if self.main_menu.get_state() == self.MAIN_MENU:
            self.game_state = self.MAIN_MENU
        elif self.main_menu.get_state() == self.GAMEPLAY_1:
            self.map = Map(self.screen)
            self.map.create_countries()
            self.map.set_state(self.GAMEPLAY_1)
            # When decision on number of players has been done it passes it to Map
            self.map.set_players_and_ai(self.main_menu.get_num_players(), self.main_menu.get_num_ai_players())
            self.map.create_players()
            # Define players
            self.players = self.map.get_players()
            self.deal_initial_troops_to_players()
            self.game_state = self.GAMEPLAY_1
        elif self.main_menu.get_state() == self.GAMEPLAY_2:
            self.map = Map(self.screen)
            self.map.create_countries()
            self.map.set_state(self.GAMEPLAY_2)
            self.map.set_players_and_ai(self.main_menu.get_num_players(), self.main_menu.get_num_ai_players())
            self.map.create_players()
            self.players = self.map.get_players()
            self.deal_initial_troops_to_players()
            self.game_state = self.GAMEPLAY_2
        elif self.main_menu.get_state() == self.EXIT:
            self.game_state = self.EXIT

    # Keeps track of current game states in objects and activates necessary functions during GAMEPLAY1 state
    def check_state_gameplay(self):
        if self.map.get_state() == self.MAIN_MENU:
            self.gameplay_stage = self.CHOOSE_FIRST_TURN
            self.game_state = self.MAIN_MENU
            self.main_menu.change_state(self.game_state)
        elif self.game_state == self.GAMEPLAY_1:
            if self.gameplay_stage == self.CHOOSE_FIRST_TURN:
                self.choose_first_turn()
        elif self.game_state == self.GAMEPLAY_2:
            if self.gameplay_stage == self.CHOOSE_FIRST_TURN:
                self.choose_first_turn()
            elif self.gameplay_stage == self.SETUP:
                if not self.countries_divided and len(self.map.countries) == 42:
                    self.divide_countries()
                    self.countries_divided = True

    # pass turn to the next player
    def pass_turn(self):
        if self.current_turn == len(self.players) - 1:
            self.current_turn = 0
        else:
            self.current_turn += 1
        self.map.change_turn(self.current_turn)

    # This function handles the decision on which player goes first
    def choose_first_turn(self):
        self.map.change_turn(self.dice_throw_index)
        if self.dice_throw_index < len(self.players) and not self.showing_dice_animation:
            total = [self.dice.throw() for _ in range(3)]  # makes list of 3 random dice values, like 3 dice thrown
            self.dice_thrown.append(total)
            self.showing_dice_animation = True
            self.animation_start_time = pygame.time.get_ticks()
        elif self.showing_dice_animation:
            if pygame.time.get_ticks() - self.animation_start_time >= 2500:  # 1 seconds
                self.showing_dice_animation = False
                self.dice_throw_index += 1
                if self.dice_throw_index >= len(self.players):
                    self.current_turn = self.dice_thrown.index(max(self.dice_thrown))
                    self.map.change_turn(self.current_turn)
                    self.dice_thrown = []
                    self.dice_throw_index = 0
                    self.gameplay_stage = self.SETUP

    def dice_animate(self):
        if self.showing_dice_animation:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_start_time < 3000:  # 2 seconds
                # Call the dice.animation method to display the animation
                self.dice.animation(self.dice_thrown[-1], self.players[self.dice_throw_index].get_color_name())
            else:
                self.showing_dice_animation = False

    # Specific function for 2 player game.
    # it sets randomly initial 14 owned countries to each player and sets the rest as neutral.
    # Adds 1 troop to each country
    def divide_countries(self):
        rand_ints = random.sample(range(0, 42), 42)
        part_size = len(rand_ints) // 3
        set1 = rand_ints[:part_size]
        set2 = rand_ints[part_size:part_size*2]
        set3 = rand_ints[part_size*2:]
        for country_index in set1:
            self.map.countries[country_index].set_owner(self.players[0])
            self.map.countries[country_index].add_troops(1)
            self.players[0].remove_avail_troop()
            self.players[0].add_country(self.map.countries[country_index])
        for country_index in set2:
            self.map.countries[country_index].set_owner(self.players[1])
            self.map.countries[country_index].add_troops(1)
            self.players[1].remove_avail_troop()
            self.players[1].add_country(self.map.countries[country_index])
        for country_index in set3:
            self.map.countries[country_index].add_troops(1)
        self.countries_divided = True

    # Gives certain amount of available troops to the players
    # Players placing their troops until no available troops remain
    # Then switching to the next gameplay stage
    def occupy_country(self, country):
        current_player = self.players[self.current_turn]
        if current_player.troops_available > 0:
            if len(self.map.countries) == 42:
                # Occupying neutral countries during setup is only available in 3-6 player mode
                if country.owner is None and self.game_state == self.GAMEPLAY_1:
                    country.set_owner(current_player)
                    country.add_troops(1)
                    current_player.remove_avail_troop()
                    current_player.add_country(country)
                    self.pass_turn()
                elif country.owner is not current_player:
                    print("You are doing something naughty!")
                else:
                    country.add_troops(1)
                    current_player.remove_avail_troop()
                    self.pass_turn()
        else:
            self.gameplay_stage = self.ATTACK

    # This function is specifically for country buttons
    # It triggers different methods depending on gameplay stage
    def handle_country_clicks(self, mouse_pos):
        if self.map.countries is not None:
            for country in self.map.countries:
                if country.country_btn.rect.collidepoint(mouse_pos):
                    if self.gameplay_stage == self.SETUP:
                        self.occupy_country(country)

    # Depending on number of players it deals different amount of initial troops during setup
    def deal_initial_troops_to_players(self):
        troops = 0
        if len(self.players) == 2:
            troops = 40
        elif len(self.players) == 3:
            troops = 35
        elif len(self.players) == 4:
            troops = 30
        elif len(self.players) == 5:
            troops = 25
        elif len(self.players) == 6:
            troops = 20
        for player in self.players:
            player.add_avail_troops(troops)
