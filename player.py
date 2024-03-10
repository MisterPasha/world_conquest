import pygame  # Import the pygame library for game development
from main_menu import draw_text  # Import draw_text function from main_menu module
from dice import Dice  # Import Dice class from dice module

# Initialize pygame
pygame.init()


# Super Class for Human and AI agent
# Only holds methods and attributes that both Human and AI players will have in common


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

    def add_avail_troops(self, num_of_troops):
        """
        Adds troops that need to be placed
        :param num_of_troops: Number of troops to add
        :return:
        """
        self.troops_available += num_of_troops

    def remove_avail_troop(self):
        """
        Removes one troop from available troops and adds it to held troops
        :return:
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
        :return:
        """
        self.pos = (x, y)
        self.size = (width, height)
        self.profile = pygame.transform.scale(self.profile, self.size)

    def draw_profile(self):
        """
        Draws profiles on the map
        :return:
        """
        self.screen.blit(self.profile, self.pos)
        # Draw the text indicating the number of troops held by the player
        draw_text(
            self.screen,  # Pygame screen surface
            f"troops: {self.troops_holds}",
            int(self.size[0] * 0.45),  # Font size
            (0, 0, 0),
            int(self.pos[0] * 0.92),  # X position of the text (aligned to the right of the profile image)
            int(self.pos[1] + 10),  # Y position of the text (slightly below the profile image)
        )
        # Draw the text indicating the number of troops available for placement
        draw_text(
            self.screen,
            f"available: {self.troops_available}",
            int(self.size[0] * 0.45),
            (0, 0, 0),
            int(self.pos[0] * 0.92),
            int(self.pos[1] + 30),
        )

    def get_color(self):
        """
        Get player's color as RGB tuple
        :return:
        """
        return self.color

    def get_color_name(self):
        """
        Get player's color name
        :return:
        """
        return self.color_str

    def add_country(self, country):
        """
        Add country to player's owned countries
        :param country: Country object to add
        :return:
        """
        self.countries.append(country)

    def remove_country(self, country):
        """
        Remove country from player's owned countries
        :param country: Country object to remove
        :return:
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
        Execute attack for AI player
        :param country: Country object to attack
        :return:
        """
        print("attack", country)
