import pygame  # Import the pygame library for game development
import random  # RNG
from main_menu import MainMenu  # Import MainMenu class from main_menu
from main_menu import draw_text  # Import draw_text class from main_menu
from map import Map  # Import the Map class from map
from dice import Dice  # Import the Dice class from dice, for rolling dice
from button import Button  # Importing Button class from button
from deck import Deck  # Import the Deck class from deck
from deck import MissionCards  # Import the MissionCards class from deck
from player import AI  # Import the AI class from player

# Initialize pygame
pygame.init()


class Game:
    win_window = pygame.image.load("images\\win_window.png")
    paper_img = pygame.image.load("images\\gameplay_paper.png")
    button_image = pygame.image.load("images\\button_high.png")
    button_hover_image = pygame.image.load("images\\button_hover.png")
    opt_window_paper_image = pygame.image.load("images\\new_game_paper_resized.png")
    notif_edit_img = pygame.image.load("images\\notification_edit_map.png")
    notif_click_img = pygame.image.load("images\\notification_clicks.png")
    font1 = "fonts\\font1.ttf"

    # Game States
    EXIT = -1
    MAIN_MENU = 0
    GAMEPLAY_1 = 1  # 3-6 players game
    GAMEPLAY_2 = 2  # 2 players game

    # Gameplay stages
    CHOOSE_FIRST_TURN = 0
    SETUP = 1
    DRAFT = 2
    ATTACK = 3
    FORTIFY = 4
    EDIT = 5
    HOLD = 6
    GAME_OVER = 7

    def __init__(self, screen, clock, window_size):
        """
        Initializes the game instance with necessary attributes
        :param screen: Pygame display surface
        :param clock: Managing time
        :param window_size: Tuple containing width and height of the game window
        """
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.running = True

        # image paper in gameplay
        self.paper_img = pygame.transform.scale(
            self.paper_img, (screen.get_width(), screen.get_height())
        )
        self.win_window = pygame.transform.scale(
            self.win_window, (screen.get_width(), screen.get_height())
        )
        self.opt_window_paper_image = pygame.transform.scale(
            self.opt_window_paper_image,
            (int(screen.get_width() * 0.07), int(screen.get_height() * 0.2)),
        )
        self.change_name_window = pygame.transform.scale(
            self.opt_window_paper_image,
            (int(screen.get_width() * 0.18), int(screen.get_height() * 0.17)),
        )
        self.notif_edit_img = pygame.transform.scale(
            self.notif_edit_img,
            (int(screen.get_width() * 0.2), int(screen.get_height() * 0.2)),
        )
        self.notif_click_img = pygame.transform.scale(
            self.notif_click_img,
            (int(screen.get_width() * 0.2), int(screen.get_height() * 0.2)),
        )

        # set initial state
        self.game_state = self.MAIN_MENU

        # set initial gameplay stage
        self.gameplay_stage = self.CHOOSE_FIRST_TURN

        # List of Player objects
        self.players = None

        # Winner Player object
        self.winner = None

        # Current player
        self.current_turn = 0
        self.turn = 0

        # initialise MainMenu object
        self.main_menu = MainMenu(self.screen)

        # initialise Map object
        self.map = None
        self.countries_divided = False
        self.opt_window = False

        # All necessary dice attributes
        self.dice = Dice(self.screen)
        # Dice attributes for first turn selection
        self.showing_dice_animation = False
        self.animation_start_time = None
        self.dice_thrown = []
        self.dice_throw_index = 0
        # Lists of dice during attacking phase
        self.attack_dice = []
        self.defend_dice = []

        # Attributes for attacking phase
        self.country_selected = None  # Holds country that is currently selected
        self.selected = False  # Boolean whether any country is selected

        # Boolean whether any country has been captured now, used when moving troops to captured country
        self.captured = False
        # Holds captured country
        self.captured_country = None
        # Counts how many countries the player captured during his turn
        self.captured_countries_in_turn = 0
        # Buttons
        self.next_phase_button = self.create_next_phase_button()
        (
            self.option_button,
            self.custom_button,
            self.ok_button,
            self.cancel_button,
        ) = self.create_buttons()

        # Initialise Deck object
        self.deck = Deck(self.screen)
        self.nth_set = 0  # Counter for card sets that are sold

        # Attributes for Fortify phase
        self.fortifying_country = None  # holds fortifying country
        self.fortify_counter = 0

        # Defines whether secret mission mode is enabled
        self.secret_mission_mode = False
        self.mission_card = MissionCards(self.screen)

        # input box to change name of the country
        self.input_box = None
        self.text_box_open = False
        self.user_text = ""
        self.input_font = pygame.font.Font(None, 25)

    # Main running loop
    def run(self):
        """
        Runs The whole logic of the game
        :return: [NONE]
        """
        while self.running:
            self.events()
            self.draw()
            self.clock.tick(60)
            if (
                self.players
                and len(self.players) <= 1
                and self.game_state != self.MAIN_MENU
            ):
                self.gameplay_stage = self.GAME_OVER
                self.winner = self.players[0]
                self.draw_win_window()
            elif (
                (
                    self.gameplay_stage == self.DRAFT
                    or self.gameplay_stage == self.ATTACK
                    or self.gameplay_stage == self.FORTIFY
                )
                and len(self.players) > 1
                and isinstance(self.players[self.current_turn], AI)
            ):
                self.switch_to_next_phase()
                pygame.time.delay(1000)
                # Comment out for testing ^^^^
            pygame.display.update()  # pygame.display.flip() ?

    # Controls all event types
    def events(self):
        """
        Detects events during running and handles them
        :return: [NONE]
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.game_state == self.MAIN_MENU:
                self.main_menu.check_clicks(event)
            elif (
                self.game_state == self.GAMEPLAY_1 or self.game_state == self.GAMEPLAY_2
            ):
                self.map.check_clicks(event)
                self.next_phase_button.check_click(event)
                self.option_button.check_click(event)
                self.custom_button.check_click(event)
                self.ok_button.check_click(event)
                self.cancel_button.check_click(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_country_clicks(event.pos, event.button)
                    self.handle_profile_clicks(event.pos, event.button)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode
            elif self.game_state == self.EXIT:
                self.running = False

    # Draws all elements on the screen
    def draw(self):
        """
        Draws all elements on the screen during different stages of the game
        :return: [NONE]
        """
        if self.game_state == self.MAIN_MENU:
            self.check_state_main_menu()
            self.main_menu.draw()
        if self.game_state == self.GAMEPLAY_1 or self.game_state == self.GAMEPLAY_2:
            self.check_state_gameplay()
            self.map.draw()
            self.draw_buttons()
            self.next_phase_button.draw(self.screen)
            self.draw_card_bonus_info()
            if self.text_box_open and self.gameplay_stage == self.EDIT:
                self.draw_change_name_window()
            if self.gameplay_stage == self.CHOOSE_FIRST_TURN:
                self.screen.blit(self.paper_img, (0, 0))
                self.dice_animate()
            elif self.gameplay_stage == self.ATTACK:
                self.dice.draw_dice_w(self.defend_dice)
                self.dice.draw_dice_r(self.attack_dice)
            if (
                self.secret_mission_mode
                and self.players[self.current_turn].mission_id
                and self.game_state != self.MAIN_MENU
            ):
                if self.mission_card.mission_completed(
                    self.players[self.current_turn].mission_id,
                    self.players[self.current_turn],
                ):
                    self.winner = self.players[self.current_turn]
                    self.draw_win_window()
                    self.gameplay_stage = self.GAME_OVER
            if self.gameplay_stage == self.HOLD:
                self.draw_edit_map_notification()
            elif self.gameplay_stage == self.EDIT:
                self.draw_clicks_notification()

    def check_state_main_menu(self):
        """
        Keeps track of current game states in objects and activates necessary functions.
        (for gameplay setup) during MAIN MENU state
        :return: [NONE]
        """
        if self.main_menu.get_state() == self.MAIN_MENU:
            self.game_state = self.MAIN_MENU
        elif self.main_menu.get_state() == self.GAMEPLAY_1:
            self.map = Map(self.screen)
            self.map.create_countries()
            self.secret_mission_mode = self.main_menu.secret_mission_mode
            self.map.set_state(self.GAMEPLAY_1)
            # When decision on number of players has been done it passes it to Map
            self.map.set_players_and_ai(
                self.main_menu.get_num_players(),
                self.main_menu.get_num_ai_players(),
                self.main_menu.get_player_types(),
            )
            self.map.create_players()
            # Define players
            self.players = self.map.get_players()
            self.deal_initial_troops_to_players()
            self.game_state = self.GAMEPLAY_1
            self.next_phase_button.change_text("Play")
        elif self.main_menu.get_state() == self.GAMEPLAY_2:
            self.map = Map(self.screen)
            self.map.create_countries()
            self.secret_mission_mode = self.main_menu.secret_mission_mode
            self.map.set_state(self.GAMEPLAY_2)
            self.map.set_players_and_ai(
                self.main_menu.get_num_players(),
                self.main_menu.get_num_ai_players(),
                self.main_menu.get_player_types(),
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
        :return: [NONE]
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
        if len(self.map.countries) == 42 and not self.deck.cards:
            self.deck.create_cards(self.map)

    # pass turn to the next player
    def pass_turn(self):
        """
        Passes turn to the next player
        :return: [NONE]
        """
        if self.current_turn == len(self.players) - 1:
            self.current_turn = 0
        else:
            self.current_turn += 1
        self.map.change_turn(self.current_turn)
        if (
            isinstance(self.players[self.current_turn], AI)
            and self.gameplay_stage == self.SETUP
        ):
            self.handle_ai_actions()

    def choose_first_turn(self):
        """
        This function handles the decision on which player goes first
        :return: [NONE]
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
            if pygame.time.get_ticks() - self.animation_start_time >= 2500:
                self.showing_dice_animation = False
                self.dice_throw_index += 1
                if self.dice_throw_index >= len(self.players):
                    self.current_turn = self.dice_thrown.index(max(self.dice_thrown))
                    self.map.change_turn(self.current_turn)
                    self.dice_thrown = []
                    self.dice_throw_index = 0
                    self.gameplay_stage = self.HOLD

    def dice_animate(self):
        """
        Specific function for "Choose who goes first" gameplay phase
        :return: [NONE]
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
        :return: [NONE]
        """
        rand_ints = random.sample(range(0, 42), 42)
        part_size = len(rand_ints) // 3
        set1 = rand_ints[:part_size]
        set2 = rand_ints[part_size : part_size * 2]
        set3 = rand_ints[part_size * 2 :]
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
        :return: [NONE]
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
                                if (
                                    event_button == 4
                                    and self.fortifying_country == country
                                ):
                                    self.move_troop_to_fortified()
                                elif (
                                    event_button == 5
                                    and self.fortifying_country == country
                                ):
                                    self.move_troop_from_fortified()
                        else:
                            self.select_country(country)
                    elif self.gameplay_stage == self.DRAFT:
                        if event_button == 1:
                            self.place_troop(country)
                    elif self.gameplay_stage == self.EDIT:
                        if event_button == 1:
                            if not self.text_box_open:
                                if self.selected:
                                    if country == self.country_selected:
                                        self.highlight_neighbour_countries(
                                            country, False
                                        )
                                        self.selected = False
                                    elif country.highlighted:
                                        self.remove_from_neighbours(country)
                                    elif not country.highlighted:
                                        self.add_to_neighbours(country)
                                else:
                                    self.select_country(country)
                        elif event_button == 3:
                            if self.text_box_open:
                                if self.country_selected == country:
                                    self.user_text = ""
                                    self.text_box_open = False
                                    self.selected = False
                            else:
                                self.text_box_open = True
                                self.country_selected = country
                                self.selected = True
                                self.input_box = pygame.Rect(
                                    country.country_btn.x + 60,
                                    country.country_btn.y - 30,
                                    200,
                                    34,
                                )
                                self.ok_button.change_pos(
                                    self.input_box.x, self.input_box.y + 50
                                )
                                self.cancel_button.change_pos(
                                    self.input_box.x + self.ok_button.rect.width + 10,
                                    self.input_box.y + 50,
                                )

    def change_name(self, new_name):
        """
        Changes name of the country and adapts new name in relevant data structures
        :param new_name: String
        :return: [NONE]
        """
        if (
            self.country_selected
            and new_name
            and new_name not in self.map.neighbours.keys()
        ):
            old_name = self.country_selected.get_name()
            for k, v in self.map.neighbours.items():
                for c in v:
                    if c == self.country_selected.get_name():
                        v.remove(c)
                        v.append(new_name)
            value = self.map.neighbours[self.country_selected.get_name()]
            # Remove the old key-value pair
            del self.map.neighbours[self.country_selected.get_name()]
            # Insert the value with the new key
            self.map.neighbours[new_name] = value
            for country in self.map.countries:
                if country.get_name() == self.country_selected.get_name():
                    country.country_name = new_name
                    break
            for card in self.deck.cards:
                if card.country_name == old_name:
                    card.country_name = new_name
            self.country_selected = None
            self.selected = False
            self.text_box_open = False
            self.user_text = ""

    def cancel(self):
        """
        Function for "Cancel" button in "Change country name" window.
        It cancels the input and closes window
        :return: [NONE]
        """
        self.selected = False
        self.country_selected = None
        self.text_box_open = False
        self.user_text = ""

    def add_to_neighbours(self, country):
        """
        Adds country to the selected country's "Neighbours"
        This country will be considered as neighbour country and will now be able to interact with
        :param country: The country to be added as a neighbour
        :return: [NONE]
        """
        self.map.neighbours[self.country_selected.get_name()].append(country.get_name())
        self.map.neighbours[country.get_name()].append(self.country_selected.get_name())
        country.highlighted = True

    def remove_from_neighbours(self, country):
        """
        removes country from the selected country's "Neighbours"
        This country will not be now considered as neighbour country
        :param country: The country to be removed as a neighbour
        :return: [NONE]
        """
        self.map.neighbours[self.country_selected.get_name()].remove(country.get_name())
        self.map.neighbours[country.get_name()].remove(self.country_selected.get_name())
        country.highlighted = False

    def place_troop(self, country):
        """
        Places troop to the country
        :param country: The country where the troop will be placed
        :return: [NONE]
        """
        current_player = self.players[self.current_turn]
        if current_player.troops_available > 0 and current_player == country.owner:
            country.add_troops(1)
            current_player.remove_avail_troop()

    def get_card_bonus(self):
        """
        Get next card trade bonus number
        :return: troops_to_add: int
        """
        nth_set = self.nth_set + 1
        if 0 < nth_set < 6:
            troops_to_add = nth_set * 2 + 2
        elif nth_set == 6:
            troops_to_add = 12
        else:
            troops_to_add = (nth_set - 6) * 5 + 15
        return troops_to_add

    def draw_card_bonus_info(self):
        """
        Draw next card trade bonus info
        :return: [NONE]
        """
        draw_text(
            self.screen,
            f"Next Trade: {self.get_card_bonus()}",
            30,
            (0, 0, 0),
            int(self.screen.get_width() * 0.88),
            int(self.screen.get_height() * 0.05),
        )

    def occupy_country(self, country):
        """
        Gives certain amount of available troops to the players.
        Players placing their troops until no available troops remain.
        Then switching to the next gameplay stage
        :param country: The country to be occupied
        :return: [NONE]
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
                    elif country.owner is current_player:
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

    def move_troop_to_captured(self, troops=1):
        """
        Moves troop to the captured territory during Attack
        :return: [NONE]
        """
        if self.country_selected.troops > 1:
            self.country_selected.remove_troops(troops)
            self.captured_country.add_troops(troops)

    def move_troop_from_captured(self):
        """
        Moves troop back from captured to selected territory during Attack
        :return: [NONE]
        """
        if self.captured_country.troops > len(self.attack_dice):
            self.captured_country.remove_troops(1)
            self.country_selected.add_troops(1)

    def move_troop_to_fortified(self):
        """
        Moves troop to the captured territory during Fortify
        :return: [NONE]
        """
        if self.country_selected.troops > 1:
            self.country_selected.remove_troops(1)
            self.fortifying_country.add_troops(1)

    def move_troop_from_fortified(self):
        """
        Moves troop back from captured to selected territory during Fortify
        :return: [NONE]
        """
        if self.fortifying_country.troops > 1:
            self.country_selected.add_troops(1)
            self.fortifying_country.remove_troops(1)

    def attack_country(self, country):
        """
        Simulates Attacking the country
        :param country: The country to be attacked
        :return: [NONE]
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
            print("Can't attack yourself ", country.get_name())
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
            if country.owner is not None:
                country.owner.remove_troops(defender_lost_armies)
            # If opponents country has 0 troops now, then overtake
            if country.troops <= 0:
                self.captured_country = country
                if country.owner is not None:
                    self.captured_country.owner.remove_country(country)
                    if (
                        self.captured_country.owner.troops_holds <= 0
                        or len(self.captured_country.owner.countries) <= 0
                    ):
                        self.captured_country.owner.playing = False
                        index = self.players.index(self.captured_country.owner)
                        if index < self.current_turn:
                            self.current_turn -= 1
                            self.map.current_turn -= 1
                        self.players.remove(self.captured_country.owner)
                self.captured_country.set_owner(current_player)
                current_player.add_country(self.captured_country)
                self.captured_country.add_troops(len(a))
                self.country_selected.remove_troops(len(a))
                self.highlight_captured(True)
                self.captured = True
                self.captured_countries_in_turn += 1
            if not self.captured:
                self.map.drop_highlights()
            self.selected = False
        else:
            print("You can only attack neighbour countries")

    def select_country(self, country):
        """
        When clicked on the country This function assigns it as Selected country,
        that later will be used.
        :param country: The country clicked by the player
        :return: [NONE]
        """
        current_player = self.players[self.current_turn]
        self.highlight_captured(False)
        if self.gameplay_stage != self.EDIT:
            if country.owner is not current_player:
                pass
            elif country.troops < 2:
                pass
            elif (
                self.gameplay_stage == self.ATTACK
                and not current_player.all_neighbours_owned(country, self.map)
            ):
                self.selected = True
                self.captured = False
                self.country_selected = country
                self.highlight_neighbour_countries(self.country_selected, True)
            elif self.gameplay_stage == self.FORTIFY:
                self.selected = True
                self.captured = False
                self.country_selected = country
                self.highlight_connected_countries(self.country_selected, True)
            # else:
            #     self.selected = True
            #     self.captured = False
            #     self.country_selected = country
            #     if self.gameplay_stage == self.ATTACK:
            #         self.highlight_neighbour_countries(self.country_selected, True)
            #     elif self.gameplay_stage == self.FORTIFY:
            #         self.highlight_connected_countries(self.country_selected, True)
        else:
            self.selected = True
            self.country_selected = country
            self.highlight_neighbour_countries(self.country_selected, True)

    def highlight_connected_countries(self, country, highlight):
        """
        Highlights connected countries during Fortify stage
        :param country: The country for which connected countries will be highlighted
        :param highlight: Boolean value (highlight or not)
        :return: [NONE]
        """
        adjacent_countries = []
        visited = set()

        def dfs(selected_country):
            """
            Performs DFS to find connected countries
            :param selected_country: The country from which DFS traversal starts
            :return: [NONE]
            """
            visited.add(selected_country)
            adjacent_countries.append(selected_country)
            neighbour_countries = self.map.get_neighbours_countries(selected_country)
            for neighbour in neighbour_countries:
                if (
                    neighbour not in visited
                    and neighbour.owner == selected_country.owner
                ):
                    dfs(neighbour)

        dfs(country)
        for country in adjacent_countries:
            country.highlighted = True if highlight else False

    def highlight_captured(self, highlight):
        """
        Makes colour of just captured country brighter
        :param highlight: Boolean value (highlight or not)
        :return: [NONE]
        """
        if self.captured_country:
            self.captured_country.highlighted = True if highlight else False

    def highlight_neighbour_countries(self, country, highlight):
        """
        Makes colours of neighbouring countries brighter to highlight them during attack
        :param country: country whose neighbours will be highlighted
        :param highlight: Boolean value (highlight or not)
        :return: [NONE]
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
        :return: [NONE]
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
        """
        This function is triggered when "Next Phase" button is clicked
        Switches gameplay phase to the next phase and calls relevant functions needed for
        specific phases
        :return: [NONE]
        """
        if self.gameplay_stage == self.EDIT or self.gameplay_stage == self.HOLD:
            self.gameplay_stage = self.SETUP
            self.map.drop_highlights()
            if (
                not self.countries_divided
                and len(self.map.countries) == 42
                and self.game_state == self.GAMEPLAY_2
            ):
                self.divide_countries()
                self.countries_divided = True
            self.next_phase_button.change_text("Draft")
            if isinstance(self.players[self.current_turn], AI):
                self.handle_ai_actions()
        elif (
            self.gameplay_stage == self.SETUP
            and self.players[self.current_turn].troops_available == 0
        ):
            self.gameplay_stage = self.DRAFT
            # Give bonus troops for number of countries
            num_of_avail_troops = self.players[
                self.current_turn
            ].calculate_num_of_draft_troops()
            self.players[self.current_turn].add_avail_troops(num_of_avail_troops)
            # Give bonus armies for captured continent
            current_player_continents = self.players[self.current_turn].continents
            if current_player_continents:
                for continent in current_player_continents:
                    self.players[self.current_turn].add_avail_troops(
                        continent.get_bonus()
                    )
            # Deal mission cards to players
            if self.secret_mission_mode:
                self.deal_mission_cards()
            self.next_phase_button.change_text("Attack")
            if isinstance(self.players[self.current_turn], AI):
                self.handle_ai_actions()
        elif self.gameplay_stage == self.ATTACK:
            self.gameplay_stage = self.FORTIFY
            self.next_phase_button.change_text("End")
            # If at least one country has been captured by current player he gets a card
            if self.captured_countries_in_turn > 0:
                self.players[self.current_turn].add_card(self.deck.get_card())
            if len(self.players[self.current_turn].cards) > 5:
                self.players[self.current_turn].sell_cards(self.nth_set, self.deck)
                self.nth_set += 1
            self.captured_countries_in_turn = 0
            self.map.drop_highlights()
            self.selected = False
            if isinstance(self.players[self.current_turn], AI):
                self.handle_ai_actions()
        elif self.gameplay_stage == self.FORTIFY:
            self.gameplay_stage = self.DRAFT
            self.pass_turn()
            self.turn += 1
            num_of_avail_troops = self.players[
                self.current_turn
            ].calculate_num_of_draft_troops()
            self.players[self.current_turn].add_avail_troops(num_of_avail_troops)
            # Give bonus armies for captured continent
            current_player_continents = self.players[self.current_turn].continents
            if current_player_continents:
                for continent in current_player_continents:
                    self.players[self.current_turn].add_avail_troops(
                        continent.get_bonus()
                    )
            self.country_selected = None
            self.next_phase_button.change_text("Attack")
            self.map.drop_highlights()
            self.fortify_counter = 0
            self.selected = False
            if isinstance(self.players[self.current_turn], AI):
                self.handle_ai_actions()
        elif (
            self.gameplay_stage == self.DRAFT
            and self.players[self.current_turn].troops_available < 1
        ):
            self.gameplay_stage = self.ATTACK
            self.next_phase_button.change_text("Fortify")
            self.map.drop_highlights()
            if isinstance(self.players[self.current_turn], AI):
                self.handle_ai_actions()

    def deal_mission_cards(self):
        """
        Randomly deals mission cards to the players
        :return: [NONE]
        """
        random_indexes = random.sample(range(1, 9), len(self.players))
        for id_, player in zip(random_indexes, self.players):
            if id_ == 7:
                player.mission_id = id_
                player.player_to_destroy = random.choice(self.players)
            else:
                player.mission_id = id_

    def create_next_phase_button(self):
        """
        Creates a button to switch between phases
        :return: button
        """
        button_image = pygame.image.load("images\\button_high.png")
        button_hover_image = pygame.image.load("images\\button_hover.png")
        width = int(self.screen.get_width() * 0.1)
        height = int(self.screen.get_height() * 0.07)
        font_size = int(self.screen.get_height() * 0.05)
        x = int(self.screen.get_width() - width)
        y = int(self.screen.get_height() * 0.7)
        button = Button(
            button_image,
            button_hover_image,
            (x, y),
            "PLAY",
            font_size,
            width,
            height,
            font=self.font1,
            action=lambda: self.switch_to_next_phase(),
        )
        return button

    def handle_profile_clicks(self, mouse_pos, event_button):
        """
        Handles player profile clicks
        Sells set of cards if you have any
        :param mouse_pos: Position of the mouse cursor
        :param event_button:
        :return: [NONE]
        """
        if self.gameplay_stage == self.DRAFT:
            if (
                self.players[self.current_turn].rect.collidepoint(mouse_pos)
                and event_button == 1
            ):
                if self.players[self.current_turn].have_set_of_cards():
                    self.nth_set += 1
                    self.players[self.current_turn].sell_cards(self.nth_set, self.deck)

    def draw_win_window(self):
        """
        Draws Win Window when someone has won
        :return: [NONE]
        """
        self.screen.blit(self.win_window, (0, 0))
        draw_text(
            self.screen,
            f"{self.winner.color_str} Won!",
            int(self.screen.get_height() * 0.08),
            (128, 25, 25),
            int(self.screen.get_width() * 0.5 - 60),
            int(self.screen.get_height() * 0.5),
            font=self.font1,
        )

    def draw_edit_map_notification(self):
        """
        Draws the edit map notification
        :return: [NONE]
        """
        self.screen.blit(
            self.notif_edit_img,
            (10, self.screen.get_height() - self.notif_edit_img.get_height() - 10),
        )

    def draw_clicks_notification(self):
        """
        Draws the clicks notification
        :return: [NONE]
        """
        self.screen.blit(
            self.notif_click_img,
            (10, self.screen.get_height() - self.notif_click_img.get_height() - 10),
        )

    def set_option_window(self):
        """
        Sets Boolean for option window
        :return: [NONE]
        """
        self.opt_window = not self.opt_window

    def edit_map(self):
        """
        Enables Map editing
        :return: [NONE]
        """
        if self.gameplay_stage == self.HOLD:
            self.gameplay_stage = self.EDIT
            self.opt_window = False

    def create_buttons(self):
        """
        Creates all necessary buttons for gameplay.
        So far just back button
        :return: buttons
        """
        opt = Button(
            self.button_image,
            self.button_hover_image,
            (10, 10),
            "| | |",
            int(self.screen.get_height() * 0.05),
            int(self.screen.get_width() * 0.05),
            int(self.screen.get_height() * 0.05),
            font=self.font1,
            action=lambda: self.set_option_window(),
        )
        customise = Button(
            self.button_image,
            self.button_hover_image,
            (20, int(self.screen.get_height() * 0.1)),
            "Edit",
            int(self.screen.get_height() * 0.04),
            int(self.screen.get_width() * 0.05),
            int(self.screen.get_height() * 0.05),
            font=self.font1,
            action=lambda: self.edit_map(),
        )
        ok = Button(
            self.button_image,
            self.button_hover_image,
            (0, 0),
            "Ok",
            int(self.screen.get_height() * 0.03),
            int(self.screen.get_width() * 0.05),
            int(self.screen.get_height() * 0.05),
            font=self.font1,
            action=lambda: self.change_name(self.user_text),
        )
        cancel = Button(
            self.button_image,
            self.button_hover_image,
            (0, 0),
            "Cancel",
            int(self.screen.get_height() * 0.03),
            int(self.screen.get_width() * 0.05),
            int(self.screen.get_height() * 0.05),
            font=self.font1,
            action=lambda: self.cancel(),
        )
        return opt, customise, ok, cancel

    def draw_buttons(self):
        """
        Draws buttons
        :return: [NONE]
        """
        self.option_button.draw(self.screen)
        if self.opt_window:
            self.screen.blit(
                self.opt_window_paper_image, (10, int(self.screen.get_height() * 0.07))
            )
            self.custom_button.draw(self.screen)
            self.map.draw_button()
        if self.gameplay_stage == self.EDIT:
            draw_text(
                self.screen,
                "Map Editor Mode",
                int(self.screen.get_height() * 0.08),
                (0, 0, 0),
                int(self.screen.get_width() * 0.35),
                int(self.screen.get_height() * 0.01),
            )

    def draw_change_name_window(self):
        """
        Draws window to change a country name
        :return: [NONE]
        """
        txt_surface = self.input_font.render(self.user_text, True, (0, 0, 0))
        self.screen.blit(
            self.change_name_window,
            (
                self.country_selected.country_btn.x + 50,
                self.country_selected.country_btn.y - 40,
            ),
        )
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box, 2)
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        self.ok_button.draw(self.screen)
        self.cancel_button.draw(self.screen)

    def handle_ai_actions(self):
        """
        Handles AI bot actions during different gameplay phases
        :return: [NONE]
        """
        ai = self.players[self.current_turn]
        if self.gameplay_stage == self.SETUP:
            ai.occupy_country(self.map, self.game_state == self.GAMEPLAY_1)
            for player in self.players:
                if player.troops_available > 0:
                    self.pass_turn()
                    break
        elif self.gameplay_stage == self.DRAFT:
            if ai.have_set_of_cards():
                self.nth_set += 1
                ai.sell_cards(self.nth_set, self.deck)
            while ai.troops_available > 0:
                ai.occupy_country(self.map, self.game_state == self.GAMEPLAY_1)
        elif self.gameplay_stage == self.ATTACK:
            attacking = True
            prob = 0.7
            while attacking:
                attacking_country, defending_country = ai.choose_country_to_attack(
                    self.map
                )
                self.country_selected = attacking_country
                if self.country_selected:
                    while attacking_country.troops > 1 and not self.captured:
                        self.attack_country(defending_country)
                    if self.captured:
                        num_of_troops = random.randint(0, attacking_country.troops - 1)
                        self.move_troop_to_captured(troops=num_of_troops)
                        self.captured = False
                    if random.random() > prob:
                        attacking = False
                else:
                    attacking = False
        elif self.gameplay_stage == self.FORTIFY:
            ai.fortify(self.map)


# Finished
