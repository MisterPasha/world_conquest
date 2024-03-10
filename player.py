import pygame
from main_menu import draw_text
from dice import Dice

pygame.init()

# Super Class for Human and AI agent
# Only holds methods and attributes that both Human and AI players will have in common


class Player:
    def __init__(self, screen, profile_img, color, color_str):
        """

        :param screen:
        :param profile_img:
        :param color:
        :param color_str:
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
        :param num_of_troops:
        :return:
        """
        self.troops_available += num_of_troops

    def remove_avail_troop(self):
        """

        :return:
        """
        self.troops_available -= 1
        self.troops_holds += 1

    def set_pos_size(self, x, y, width, height):
        """
        Set Position and size of the profile image
        :param x:
        :param y:
        :param width:
        :param height:
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
        draw_text(
            self.screen,
            f"troops: {self.troops_holds}",
            int(self.size[0] * 0.45),
            (0, 0, 0),
            int(self.pos[0] * 0.92),
            int(self.pos[1] + 10),
        )
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

        :return:
        """
        return self.color

    def get_color_name(self):
        """

        :return:
        """
        return self.color_str

    def add_country(self, country):
        """

        :param country:
        :return:
        """
        self.countries.append(country)

    def remove_country(self, country):
        """

        :param country:
        :return:
        """
        self.countries.remove(country)


class Human(Player):
    def __init__(self, screen, profile_img, color, color_str):
        """

        :param screen:
        :param profile_img:
        :param color:
        :param color_str:
        """
        super().__init__(screen, profile_img, color, color_str)

    def attack(self, my_country, defending_country):
        """
        :param my_country:
        :param defending_country:
        :return:
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

        :param screen:
        :param profile_img:
        :param color:
        :param color_str:
        """
        super().__init__(screen, profile_img, color, color_str)

    def attack(self, country):
        """

        :param country:
        :return:
        """
        print("attack", country)
