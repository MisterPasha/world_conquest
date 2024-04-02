import pygame  # Import the pygame library for game development
from main_menu import draw_text  # Import draw_text function from main_menu
from dice import Dice  # Import Dice class from dice
from collections import Counter
from map import create_continents
from deck import MissionCards
import random
import math

# Initialize pygame
pygame.init()


# Super Class for Human and AI agent
# Only holds methods and attributes that both Human and AI players will have in common

new_game_paper = pygame.image.load("images\\new_game_paper_resized.png")


class Player:
    def __init__(self, screen, profile_img, color, color_str):
        """
        Initialize Player object with common attributes
        :param screen: Pygame screen surface
        :param profile_img: Image representing player's profile
        :param color: RGB color tuple representing player's color
        :param color_str: String representing player's colour name
        """
        self.screen = screen
        self.profile = profile_img
        self.color = color
        self.color_str = color_str

        # Keeps track whether player still in the game
        self.playing = True

        # Troops that player has in the game
        self.troops_holds = 0

        # Troops that need to be placed yet
        self.troops_available = 0

        # list of Card objects that player holds
        self.cards = []

        # list of Country objects that player holds
        self.countries = []

        # list of Continents that player holds
        self.continents = []

        # Position and size of the profile image
        self.pos = None
        self.size = None
        self.rect = None
        self.info_window = pygame.image.load("images\\info_table.png")
        self.info_window = pygame.transform.scale(
            self.info_window,
            (int(screen.get_width() * 0.55), int(screen.get_height() * 0.25)),
        )

        # For game with mission cards
        self.mission_card = MissionCards(self.screen)
        self.mission_id = None
        self.player_to_destroy = None  # Needed for one of the mission cards

    def remove_troops(self, num_of_troops):
        """
        Removes a troop
        :param num_of_troops:
        :return:
        """
        self.troops_holds -= num_of_troops

    def add_card(self, card):
        """
        Adds a card to the player's collection
        :param card: The card to be added
        :return: [NONE]
        """
        self.cards.append(card)

    def add_avail_troops(self, num_of_troops):
        """
        Adds troops that need to be placed.
        'self.troops_available' is updated
        :param num_of_troops: Number of troops to add
        :return: [NONE]
        """
        self.troops_available += num_of_troops

    def remove_avail_troop(self):
        """
        Removes one troop from available troops and adds it to held troops.
        'self.troops_available' & 'self.troops_holds' is updated
        :return: [NONE]
        d
        """
        self.troops_available -= 1
        self.troops_holds += 1

    def set_pos_size(self, x, y, width, height):
        """
        Set Position and size of the profile image
        :param x: X coordinate of the position
        :param y: Y coordinate of the position
        :param width: Width of the image
        :param height: Height of the image
        :return: [NONE]
        """
        self.pos = (x, y)
        self.size = (width, height)
        self.profile = pygame.transform.scale(self.profile, self.size)
        self.rect = self.profile.get_rect(topleft=self.pos)

    def draw_profile(self):
        """
        Draws the player's profile on the map along with additional information. This method draws the profile image
        on the screen and displays the number of troops held by the player and the number of troops available for
        placement it also displays any cards the player holds when the mouse is over the profile
        :return: [NONE]
        """
        self.screen.blit(self.profile, self.pos)
        # Draw the text indicating the number of troops held by the player

        # Draw the text indicating the number of troops available for placement
        draw_text(
            self.screen,
            f"{self.troops_available}",
            int(self.size[0] * 0.45),
            (0, 0, 0),
            int(self.pos[0] * 0.98),
            int(self.pos[1] + 35),
        )

        # If the mouse is over the profile, display the information window and any cards the player holds
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.info_window, (int(self.screen.get_width() * 0.35), self.pos[1]))
            # Draw the text indicating the number of troops held by the player
            draw_text(
                self.screen,  # Pygame screen surface
                f"{self.troops_holds}",
                int(self.size[0] * 0.7),  # Font size
                (173, 28, 28),
                int(int(self.screen.get_width() * 0.35) + self.info_window.get_width() * 0.87),
                int(self.pos[1] + self.info_window.get_height() * 0.7),
            )
            draw_text(
                self.screen,  # Pygame screen surface
                f"{len(self.countries)}",
                int(self.size[0] * 0.7),  # Font size
                (173, 28, 28),
                int(int(self.screen.get_width() * 0.35) + self.info_window.get_width() * 0.87),
                int(self.pos[1] + self.info_window.get_height() * 0.3),
            )
            for i, card in enumerate(self.cards):
                card.draw(int(self.screen.get_width() * 0.37) + i * card.width,
                          self.pos[1] + self.info_window.get_height() * 0.1)
            if self.mission_id:
                if self.mission_id == 7:
                    self.mission_card.draw(self.mission_id, int(self.screen.get_width() * 0.27),
                                           int(self.pos[1] + self.info_window.get_height() * 0.1),
                                           self.player_to_destroy.color_str)
                else:
                    self.mission_card.draw(self.mission_id, int(self.screen.get_width() * 0.27),
                                           int(self.pos[1] + self.info_window.get_height() * 0.1))

    def calculate_num_of_draft_troops(self):
        """
        Calculates a number of troops to get during Draft phase
        :return: num_of_avail_troops
        """
        num_of_avail_troops = len(self.countries) // 3
        num_of_avail_troops = num_of_avail_troops if num_of_avail_troops > 3 else 3
        return num_of_avail_troops

    def find_continents(self):
        """
        Checks which continents player holds and adds/removes them to the list
        :return:
        """
        continents = create_continents()
        continents_held = []
        countries_held = [country.country_name for country in self.countries]
        for continent in continents:
            # Check if the player holds all countries in the continent
            if all(country in countries_held for country in continent.countries_in_continent):
                continents_held.append(continent)
        self.continents = continents_held

    def have_set_of_cards(self):
        """
        Checks if player has a set of cards
        :return: boolean
        """
        cards = [card.army_type for card in self.cards]
        card_dict = Counter(cards)
        wild_cards = card_dict["Wild"]
        for k, v in card_dict.items():
            if v >= 3 or len(card_dict) >= 3 or v + wild_cards >= 3:
                return True
        return False

    def remove_set_cards(self, army_type, deck):
        """
        Removes set of same cards from the hand
        :param army_type:
        :param deck:
        :return:
        """
        counter = 0
        bonus_counter = 0
        cards_to_remove = []
        for card in self.cards:
            if card.army_type == army_type or card.army_type == "Wild":
                if counter < 3:
                    deck.cards.append(card)
                    cards_to_remove.append(card)
                    counter += 1
                    if bonus_counter < 1:
                        for country in self.countries:
                            if country.country_name == card.country_name:
                                country.add_troops(2)
                                self.troops_holds += 2
                                bonus_counter += 1
        for card in cards_to_remove:
            self.cards.remove(card)

    def all_neighbours_owned(self, country, map_):
        neighbour_countries = map_.get_neighbours_countries(country)
        for c in neighbour_countries:
            if c not in self.countries:
                return False
        return True

    def remove_distinct_cards(self, deck):
        """
        removes a set of distinct cards from the hand
        :param deck:
        :return:
        """
        distinct_types = set()
        distinct_cards = []
        bonus_counter = 0
        for card in self.cards:
            if card.army_type not in distinct_types and len(distinct_cards) < 3:
                distinct_cards.append(card)
                distinct_types.add(card.army_type)
                deck.cards.append(card)
                if bonus_counter < 1:
                    for country in self.countries:
                        if country.country_name == card.country_name:
                            country.add_troops(2)
                            self.troops_holds += 2
                            bonus_counter += 1
            elif card.army_type == "Wild":
                distinct_cards.append(card)
        for card in distinct_cards:
            self.cards.remove(card)

    def sell_cards(self, nth_set, deck):
        """
        Exchanges set of cards for the troops
        :param nth_set:
        :param deck:
        :return:
        """
        cards = [card.army_type for card in self.cards]
        card_dict = Counter(cards)
        wild_cards = card_dict["Wild"] - 1 if card_dict["Wild"] > 1 else card_dict["Wild"]
        if max(card_dict.values()) >= 3:
            army_type = max(card_dict, key=card_dict.get)
            self.remove_set_cards(army_type, deck)
        elif len(card_dict) + wild_cards >= 3:
            self.remove_distinct_cards(deck)

        self.add_avail_troops(self.get_card_bonus(nth_set))

    def get_card_bonus(self, nth_set):
        """
        Gives number of troops from selling cards
        :param nth_set:
        :return: troops_to_add
        """
        if 0 < nth_set < 6:
            troops_to_add = nth_set * 2 + 2
        elif nth_set == 6:
            troops_to_add = 12
        else:
            troops_to_add = (nth_set - 6) * 5 + 15
        return troops_to_add

    def get_color(self):
        """
        Get player's colour as RGB tuple
        :return: Player's colour
        """
        return self.color

    def get_color_name(self):
        """
        Get players colour's name
        :return: Name of the player's colour
        """
        return self.color_str

    def add_country(self, country):
        """
        Add country to player's owned countries
        :param country: Country object to add
        :return: [NONE]
        """
        self.countries.append(country)
        self.find_continents()

    def remove_country(self, country):
        """
        Remove country from player's owned countries
        :param country: Country object to remove
        :return: [NONE]
        """
        self.countries.remove(country)
        self.find_continents()

    def attack(self, my_country, defending_country):
        """
        Execute attack between human player's country and defending country
        :param my_country: Player's country object
        :param defending_country: Defending country object
        :return: Tuple containing information about the outcome of the attack
        """
        die = Dice(self.screen)

        # define number of attacking troops (Should be chosen by player, but hardcoded for now)
        attackers = my_country.troops - 1 if my_country.troops <= 3 else 3
        # define number of defending troops (Should be chosen by player, but hardcoded for now)
        defenders = defending_country.troops if defending_country.troops <= 2 else 2

        attack_dice_values = [die.throw() for _ in range(attackers)]
        defend_dice_values = [die.throw() for _ in range(defenders)]

        # sort values in descending order to compare dice
        sorted_attack_values = sorted(attack_dice_values, reverse=True)
        sorted_defend_values = sorted(defend_dice_values, reverse=True)

        # Initialize counters for lost troops
        attacker_lost_armies = 0
        defender_lost_armies = 0

        # Compare dice rolls
        for a_value, d_value in zip(sorted_attack_values, sorted_defend_values):
            if a_value > d_value:
                defender_lost_armies += 1
            else:
                attacker_lost_armies += 1

        return (
            attacker_lost_armies,
            defender_lost_armies,
            attack_dice_values,
            defend_dice_values,
        )


class Human(Player):
    def __init__(self, screen, profile_img, color, color_str):
        """
        Initialize Human player object
        :param screen: Pygame screen surface
        :param profile_img: Image representing player's profile
        :param color: RGB color tuple representing player's color
        :param color_str: String representing player's color name
        """
        super().__init__(screen, profile_img, color, color_str)


class AI(Player):
    def __init__(self, screen, profile_img, color, color_str):
        """
        Initialize AI player object
        :param screen: Pygame screen surface
        :param profile_img: Image representing player's profile
        :param color: RGB color tuple representing player's color
        :param color_str: String representing player's color name
        """
        super().__init__(screen, profile_img, color, color_str)

    def occupy_country(self, map_, gameplay1: bool):
        """
        Occupy country during setup.
        If all countries have owner then place troop in owned country. with probability 10% it places troops
        randomly, or 90% chance on the country that is bordering enemy territory
        to bring more attacking or defending power
        :param map_: Map
        :param gameplay1: bool
        :return: [NONE]
        """
        if self.troops_available > 0:
            # Choose country that hasn't owner
            if not map_.all_countries_have_owner() and gameplay1:
                no_owner_countries = set()
                for country in map_.countries:
                    if not country.owner:
                        no_owner_countries.add(country)
                selected_country = random.choice(list(no_owner_countries))
                self.countries.append(selected_country)
                selected_country.set_owner(self)
                selected_country.add_troops(1)
                self.remove_avail_troop()
            # If all countries have owner then place troop in owned country
            else:
                prob = 0.9
                if random.random() > prob:
                    selected_country = random.choice(self.countries)
                    selected_country.add_troops(1)
                    self.remove_avail_troop()
                else:
                    potential_countries = []
                    for country in self.countries:
                        neighbour_countries = map_.get_neighbours_countries(country)
                        for n_country in neighbour_countries:
                            if n_country.owner != self:
                                potential_countries.append(country)
                                break
                    selected_country = random.choice(potential_countries)
                    selected_country.add_troops(1)
                    self.remove_avail_troop()

    def choose_country_to_attack(self, map_):
        """
        This function is choosing attacking country and defending country.
        First it finds all countries that bordering enemy territories and filters out potential countries to attack
        by checking their number of troops, it will not consider enemy countries that have higher number of troops
        or have more than 80% of attacking country troops, as it can lead to loosing the battle.
        If it cannot find any suitable countries to attack it won't attack at all.
        In 70% chance it will attack the country with least number of troops. And 30% chance it will choose randomly.

        :param map_: Map
        :return: Attacking Country, Defending Country
        """
        attack_defend_countries = {}
        found = False
        i = 0
        attacking_country = None
        for country in self.countries:
            if country.troops > 1:
                neighbour_countries = map_.get_neighbours_countries(country)
                for c in neighbour_countries:
                    if c.owner is not self or not c.owner:
                        attack_defend_countries.setdefault(country, []).append(c)
        for k, v in attack_defend_countries.items():
            for country in v[:]:
                if country.troops >= k.troops or country.troops > math.ceil(k.troops * 0.8):
                    attack_defend_countries[k].remove(country)
        while not found and i < 100 and attack_defend_countries:
            attacking_country = random.choice(list(attack_defend_countries.keys()))
            if len(attack_defend_countries[attacking_country]) > 0:
                found = True
            else:
                i += 1
        if not found:
            return None, None
        else:
            prob = 0.7
            if random.random() > prob:
                defending_country = random.choice(attack_defend_countries[attacking_country])
            else:
                defending_country = attack_defend_countries[attacking_country][0]
                least_troops = attack_defend_countries[attacking_country][0].troops
                for country in attack_defend_countries[attacking_country]:
                    if country.troops <= least_troops:
                        least_troops = country.troops
                        defending_country = country
            return attacking_country, defending_country

    def fortify(self, map_):
        fortify_to_country = None
        fortify_from_country = None
        potential_countries = {}
        for country in self.countries:
            if country.troops > 1:
                potential_countries[country] = country.troops
        potential_countries = sorted(potential_countries.items(), key=lambda item: item[1], reverse=True)
        potential_countries = dict(potential_countries)

        for country, value in potential_countries.items():
            neighbour_countries = map_.get_neighbours_countries(country)
            have_enemy_in_neighbour = False
            for n_country in neighbour_countries:
                if n_country.owner != self:
                    have_enemy_in_neighbour = True
                    break
            if not have_enemy_in_neighbour:
                fortify_from_country = country
                break
        if fortify_from_country:
            connected_dict = {}
            connected_countries = map_.get_connected_countries(fortify_from_country)
            for country in connected_countries:
                connected_dict[country] = country.troops
            connected_dict = sorted(potential_countries.items(), key=lambda item: item[1])
            connected_dict = dict(connected_dict)
            for country in connected_dict.keys():
                neighbour_countries = map_.get_neighbours_countries(country)
                have_enemy_in_neighbour = False
                for n_country in neighbour_countries:
                    if n_country.owner != self:
                        have_enemy_in_neighbour = True
                if have_enemy_in_neighbour:
                    fortify_to_country = country
                    break
        if fortify_to_country and fortify_from_country:
            prob = 0.8
            fortify_to_country.highlighted = True
            fortify_from_country.highlighted = True
            if random.random() < prob:
                fortify_to_country.add_troops(fortify_from_country.troops - 1)
                fortify_from_country.remove_troops(fortify_from_country.troops - 1)
            else:
                num_of_troops = random.randint(1, fortify_from_country.troops - 1)
                fortify_to_country.add_troops(num_of_troops)
                fortify_from_country.remove_troops(num_of_troops)
