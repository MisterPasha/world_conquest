import pygame
import random
from main_menu import MainMenu
from map import Map
from dice import Dice
from button import Button
from deck import Deck

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
        """

        :param screen:
        :param clock:
        :param window_size:
        """
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.running = True
        # image paper in gameplay
        self.paper_img = pygame.transform.scale(
            self.paper_img, (screen.get_width(), screen.get_height())
        )
        # set initial state
        self.game_state = self.MAIN_MENU
        # set initial gameplay stage
        self.gameplay_stage = self.CHOOSE_FIRST_TURN
        # List of Player objects
        self.players = None
        # Current player
        self.current_turn = 0
        self.turn = 0
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
        self.attack_dice = []
        self.defend_dice = []
        # Attributes for attacking phase
        self.country_selected = None  # Holds country that is currently selected
        self.selected = False  # Boolean whether any country is selected
        # Boolean whether any country has been captured now, used when moving troops to captured country
        self.captured = False
        self.captured_country = None
        self.captured_countries_in_turn = 0
        self.next_phase_button = self.create_next_phase_button()
        # Initialise Deck object
        self.deck = Deck(self.screen)
        # Attributes for Fortify phase
        self.fortifying_country = None
        self.fortify_counter = 0

    # Main running loop
    def run(self):
        """

        :return:
        """
        while self.running:
            self.events()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()  # pygame.display.flip() ?

    # Controls all event types
    def events(self):
        """

        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.game_state == self.MAIN_MENU:
                self.main_menu.check_clicks(event)
            elif self.game_state == self.GAMEPLAY_1 or self.game_state == self.GAMEPLAY_2:
                self.map.check_clicks(event)
                self.next_phase_button.check_click(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_country_clicks(event.pos, event.button)
            elif self.game_state == self.EXIT:
                self.running = False

    # Draws all elements on the screen
    def draw(self):
        """

        :return:
        """
        if self.game_state == self.MAIN_MENU:
            self.check_state_main_menu()
            self.main_menu.draw()
        if self.game_state == self.GAMEPLAY_1 or self.game_state == self.GAMEPLAY_2:
            self.check_state_gameplay()
            self.map.draw()
            self.next_phase_button.draw(self.screen)
            if self.gameplay_stage == self.CHOOSE_FIRST_TURN:
                self.screen.blit(self.paper_img, (0, 0))
                self.dice_animate()
            elif self.gameplay_stage == self.ATTACK:
                self.dice.draw_dice_w(self.defend_dice)
                self.dice.draw_dice_r(self.attack_dice)

    def check_state_main_menu(self):
        """
        Keeps track of current game states in objects and activates necessary functions.
        (for gameplay setup) during MAIN MENU state
        :return:
        """
        if self.main_menu.get_state() == self.MAIN_MENU:
            self.game_state = self.MAIN_MENU
        elif self.main_menu.get_state() == self.GAMEPLAY_1:
            self.map = Map(self.screen)
            self.map.create_countries()
            self.map.set_state(self.GAMEPLAY_1)
            # When decision on number of players has been done it passes it to Map
            self.map.set_players_and_ai(
                self.main_menu.get_num_players(), self.main_menu.get_num_ai_players()
            )
            self.map.create_players()
            # Define players
            self.players = self.map.get_players()
            self.deal_initial_troops_to_players()
            self.game_state = self.GAMEPLAY_1
        elif self.main_menu.get_state() == self.GAMEPLAY_2:
            self.map = Map(self.screen)
            self.map.create_countries()
            self.map.set_state(self.GAMEPLAY_2)
            self.map.set_players_and_ai(
                self.main_menu.get_num_players(), self.main_menu.get_num_ai_players()
            )
            self.map.create_players()
            self.players = self.map.get_players()
            self.deal_initial_troops_to_players()
            self.game_state = self.GAMEPLAY_2
        elif self.main_menu.get_state() == self.EXIT:
            self.game_state = self.EXIT

    def check_state_gameplay(self):
        """
        Keeps track of current game states in objects and activates necessary functions during GAMEPLAY1 state
        :return:
        """
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
        """

        :return:
        """
        if self.current_turn == len(self.players) - 1:
            self.current_turn = 0
        else:
            self.current_turn += 1
        self.map.change_turn(self.current_turn)

    def choose_first_turn(self):
        """
        This function handles the decision on which player goes first
        :return:
        """
        self.map.change_turn(self.dice_throw_index)
        if (
                self.dice_throw_index < len(self.players)
                and not self.showing_dice_animation
        ):
            total = [
                self.dice.throw() for _ in range(3)
            ]  # makes list of 3 random dice values, like 3 dice thrown
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
        """

        :return:
        """
        if self.showing_dice_animation:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_start_time < 3000:  # 2 seconds
                # Call the dice.animation method to display the animation
                self.dice.animation(
                    self.dice_thrown[-1],
                    self.players[self.dice_throw_index].get_color_name(),
                )
            else:
                self.showing_dice_animation = False

    def divide_countries(self):
        """
        Specific function for 2 player game.
        It sets randomly initial 14 owned countries to each player and sets the rest as neutral.
        Adds 1 troop to each country
        :return:
        """
        rand_ints = random.sample(range(0, 42), 42)
        part_size = len(rand_ints) // 3
        set1 = rand_ints[:part_size]
        set2 = rand_ints[part_size: part_size * 2]
        set3 = rand_ints[part_size * 2:]
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

    def handle_country_clicks(self, mouse_pos, event_button):
        """
        This function is specifically for country buttons.
        It triggers different methods depending on gameplay stage
        :param mouse_pos: Holds mouse position coordinates
        :param event_button: Holds event button type. like left/right mouse click, wheel up/down
        :return:
        """
        if self.map.countries is not None:
            for country in self.map.countries:
                if country.country_btn.rect.collidepoint(mouse_pos):
                    if self.gameplay_stage == self.SETUP:
                        self.occupy_country(country)
                    elif self.gameplay_stage == self.ATTACK:
                        if event_button == 1:
                            if self.selected:
                                self.attack_country(country)
                            else:
                                self.select_country(country)
                        elif event_button == 4:
                            if self.captured and country.highlighted:
                                self.move_troop_to_captured()
                        elif event_button == 5:
                            if self.captured and country.highlighted:
                                self.move_troop_from_captured()
                    elif self.gameplay_stage == self.FORTIFY:
                        if self.selected:
                            if country == self.country_selected:
                                self.highlight_connected_countries(country, False)
                                self.selected = False
                            elif country.highlighted:
                                if self.fortify_counter == 0:
                                    self.fortifying_country = country
                                self.fortify_counter += 1
                                if event_button == 4 and self.fortifying_country == country:
                                    self.move_troop_to_fortified()
                                elif event_button == 5 and self.fortifying_country == country:
                                    self.move_troop_from_fortified()
                        else:
                            self.select_country(country)
                    elif self.gameplay_stage == self.DRAFT:
                        if event_button == 1:
                            self.place_troop(country)

    def place_troop(self, country):
        current_player = self.players[self.current_turn]
        if current_player.troops_available > 0 and current_player == country.owner:
            country.add_troops(1)
            current_player.remove_avail_troop()

    def occupy_country(self, country):
        """
        Gives certain amount of available troops to the players.
        Players placing their troops until no available troops remain.
        Then switching to the next gameplay stage
        :param country:
        :return:
        """
        current_player = self.players[self.current_turn]
        if current_player.troops_available > 0:
            if len(self.map.countries) == 42:
                if self.game_state == self.GAMEPLAY_1:  # 3-6 player game
                    if not self.map.all_countries_have_owner():
                        if country.owner is None:
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
                if self.game_state == self.GAMEPLAY_2:  # 2 player game
                    if country.owner is not current_player:
                        print("You are doing something naughty!")
                    else:
                        country.add_troops(1)
                        current_player.remove_avail_troop()
                        self.pass_turn()

    def move_troop_to_captured(self):
        if self.country_selected.troops > 1:
            self.country_selected.remove_troops(1)
            self.captured_country.add_troops(1)

    def move_troop_from_captured(self):
        if self.captured_country.troops > len(self.attack_dice):
            self.captured_country.remove_troops(1)
            self.country_selected.add_troops(1)

    def move_troop_to_fortified(self):
        if self.country_selected.troops > 1:
            self.country_selected.remove_troops(1)
            self.fortifying_country.add_troops(1)

    def move_troop_from_fortified(self):
        if self.fortifying_country.troops > 1:
            self.country_selected.add_troops(1)
            self.fortifying_country.remove_troops(1)

    def attack_country(self, country):
        """

        :param country:
        :return:
        """
        current_player = self.players[self.current_turn]
        if country == self.country_selected:  # Unselect Country by second click
            self.highlight_neighbour_countries(self.country_selected, False)
            self.selected = False
            # self.country_selected = None
            print("unselected")
        elif (
                country in current_player.countries
        ):  # Error message when trying to attack own country
            print("It is dumb to attack yourself")
        elif country.get_name() in self.map.get_neighbours(
                self.country_selected.get_name()
        ):  # Attack!
            attacker_lost_armies, defender_lost_armies, a, d = current_player.attack(
                self.country_selected, country
            )
            self.attack_dice = a
            self.defend_dice = d
            country.remove_troops(defender_lost_armies)
            self.country_selected.remove_troops(attacker_lost_armies)
            current_player.remove_troops(attacker_lost_armies)
            country.owner.remove_troops(defender_lost_armies)
            # If opponents country has 0 troops now, then overtake
            if country.troops <= 0:
                self.captured_country = country
                if self.game_state == self.GAMEPLAY_1:
                    self.captured_country.owner.remove_country(country)
                self.captured_country.set_owner(current_player)
                current_player.add_country(self.captured_country)
                self.captured_country.add_troops(len(a))
                self.country_selected.remove_troops(len(a))
                self.highlight_captured(True)
                self.captured = True
                self.captured_countries_in_turn += 1
            self.highlight_neighbour_countries(self.country_selected, False)
            self.selected = False
        else:
            print("You can only attack neighbour countries")

    def select_country(self, country):
        """

        :param country:
        :return:
        """
        current_player = self.players[self.current_turn]
        self.highlight_captured(False)
        if country.owner is not current_player:
            print("Can select only owned country!")
        elif country.troops < 2:
            print("Not enough troops")
        else:
            self.selected = True
            self.captured = False
            self.country_selected = country
            if self.gameplay_stage == self.ATTACK:
                self.highlight_neighbour_countries(self.country_selected, True)
            elif self.gameplay_stage == self.FORTIFY:
                self.highlight_connected_countries(self.country_selected, True)

    def highlight_connected_countries(self, country, highlight):
        adjacent_countries = []
        visited = set()

        def dfs(selected_country):
            visited.add(selected_country)
            adjacent_countries.append(selected_country)
            print("Hello")
            neighbour_countries = self.map.get_neighbours_countries(selected_country)
            for neighbour in neighbour_countries:
                print("Here1")
                if neighbour not in visited and neighbour.owner == selected_country.owner:
                    print("HERE2")
                    dfs(neighbour)

        dfs(country)
        for country in adjacent_countries:
            country.highlighted = True if highlight else False

    def highlight_captured(self, highlight):
        """
        Makes colour of just captured country brighter
        :param highlight:
        :return:
        """
        if self.captured_country:
            self.captured_country.highlighted = True if highlight else False

    def highlight_neighbour_countries(self, country, highlight):
        """
        Makes colours of neighbouring countries brighter to highlight them during attack
        :param country:
        :param highlight:
        :return:
        """
        neighbour_country_names = self.map.get_neighbours(country.get_name())
        for c in self.map.countries:
            if (
                    c.get_name() in neighbour_country_names
                    and c not in self.players[self.current_turn].countries
            ):
                c.highlighted = True if highlight else False

    def deal_initial_troops_to_players(self):
        """
        Depending on number of players it deals different amount of initial troops during setup
        :return:
        """
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

    def switch_to_next_phase(self):
        if self.gameplay_stage == self.SETUP and self.players[self.current_turn].troops_available == 0:
            self.deck.create_cards(self.map)  # Creates a deck of cards, couldn't find a better place for it :)
            self.gameplay_stage = self.ATTACK
            self.next_phase_button.change_text("To Fortify phase")
        elif self.gameplay_stage == self.ATTACK:
            self.gameplay_stage = self.FORTIFY
            self.next_phase_button.change_text("End Turn")
            # If at least one country has been captured by current player he gets a card
            if self.captured_countries_in_turn > 0:
                self.players[self.current_turn].add_card(self.deck.get_card())
            self.captured_countries_in_turn = 0
            self.map.drop_highlights()
            self.selected = False
        elif self.gameplay_stage == self.FORTIFY:
            self.gameplay_stage = self.DRAFT
            self.pass_turn()
            self.turn += 1
            if self.turn > len(self.players) - 1:
                num_of_avail_troops = self.players[self.current_turn].calculate_num_of_draft_troops()
                self.players[self.current_turn].add_avail_troops(num_of_avail_troops)
            self.country_selected = None
            self.next_phase_button.change_text("To Attack phase")
            self.map.drop_highlights()
            self.fortify_counter = 0
            self.selected = False
        elif self.gameplay_stage == self.DRAFT and self.players[self.current_turn].troops_available < 1:
            self.gameplay_stage = self.ATTACK
            self.next_phase_button.change_text("To Fortify phase")
            self.map.drop_highlights()

    def create_next_phase_button(self):
        button_image = pygame.image.load("images\\button_high.png")
        button_hover_image = pygame.image.load("images\\button_hover.png")
        x = int(self.screen.get_width() * 0.25)
        y = int(self.screen.get_height() * 0.93)
        width = int(self.screen.get_width() * 0.15)
        height = int(self.screen.get_height() * 0.07)
        font_size = int(self.screen.get_height() * 0.04)
        button = Button(button_image,
                        button_hover_image,
                        (x, y),
                        "To Attack phase",
                        font_size,
                        width,
                        height,
                        action=lambda: self.switch_to_next_phase()
                        )
        return button
