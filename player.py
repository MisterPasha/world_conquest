import pygame  # Import the pygame library for game development
from main_menu import draw_text  # Import draw_text function from main_menu
from dice import Dice  # Import Dice class from dice
from collections import Counter

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

        # Troops that player has in the game
        self.troops_holds = 0

        # Troops that need to be placed yet
        self.troops_available = 0

        # list of Card objects that player holds
        self.cards = []

        # list of Country objects that player holds
        self.countries = []

        # Position and size of the profile image
        self.pos = None
        self.size = None
        self.rect = None
        self.info_window = pygame.image.load("images\\info_table.png")
        self.info_window = pygame.transform.scale(
            self.info_window,
            (int(screen.get_width() * 0.55), int(screen.get_height() * 0.25)),
        )

    def remove_troops(self, num_of_troops):
        """

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

    def calculate_num_of_draft_troops(self):
        """

        :return:
        """
        num_of_avail_troops = len(self.countries) // 3
        num_of_avail_troops = num_of_avail_troops if num_of_avail_troops > 3 else 3
        return num_of_avail_troops

    def have_set_of_cards(self):
        """

        :return:
        """
        cards = [card.army_type for card in self.cards]
        card_dict = Counter(cards)
        wild_cards = card_dict["Wild"]
        print(card_dict)
        for k, v in card_dict.items():
            if v >= 3 or len(card_dict) >= 3 or v + wild_cards >= 3:
                return True
        return False

    def remove_set_cards(self, army_type, deck):
        """

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
                                print("bonus has been used")
        for card in cards_to_remove:
            self.cards.remove(card)

    def remove_distinct_cards(self, deck):
        """

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
                            print("bonus has been used")
            elif card.army_type == "Wild":
                distinct_cards.append(card)
        for card in distinct_cards:
            self.cards.remove(card)

    def sell_cards(self, nth_set, deck):
        """

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

    def remove_country(self, country):
        """
        Remove country from player's owned countries
        :param country: Country object to remove
        :return: [NONE]
        """
        self.countries.remove(country)


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

    def attack(self, country):
        """
        Execute attack for AI player.
        Prints the country with "attack"
        :param country: Country object to attack
        :return: [NONE]
        """
        print("attack", country)
