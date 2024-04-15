import pygame  # Import the pygame library for game development
import random  # RNG
from main_menu import draw_text  # Import draw_text class from main_menu

# Initialize pygame
pygame.init()


class Dice:
    # Loading dice face images.
    dice_w = [
        pygame.image.load("images\\die1.png"),
        pygame.image.load("images\\die2.png"),
        pygame.image.load("images\\die3.png"),
        pygame.image.load("images\\die4.png"),
        pygame.image.load("images\\die5.png"),
        pygame.image.load("images\\die6.png"),
    ]

    dice_r = [
        pygame.image.load("images\\red_die1.png"),
        pygame.image.load("images\\red_die2.png"),
        pygame.image.load("images\\red_die3.png"),
        pygame.image.load("images\\red_die4.png"),
        pygame.image.load("images\\red_die5.png"),
        pygame.image.load("images\\red_die6.png"),
    ]

    def __init__(self, screen):
        """
        Initialise DiceHandler in accordance to the screen
        + dictionary of dice images
        :param screen: Pygame screen surface
        """
        self.screen = screen
        self.dice_dict = self.create_dice()

    def throw(self):
        """
        Simulates the dice roll using random integer 1-6
        :return: 'value' The result of the role
        """
        value = random.randint(1, 6)
        return value

    def animation(self, nums, name):
        """
        Displays an animation for dice rolls
        :param nums: List of dice values rolled
        :param name: Name of the player who rolled the dice
        :return: [NONE]
        """
        draw_text(
            self.screen,
            f"{name} rolled a total of {sum(nums)}",
            int(self.screen.get_height() * 0.07),
            (133, 14, 12),
            int(self.screen.get_width() * 0.35),
            int(self.screen.get_height() * 0.7),
        )
        self.draw_dice_w(nums)

    def draw_dice_w(self, nums):
        """
        Draws the white dice images on the screen based on the rolls provided in `nums`.
        It positions each die image on the screen
        :param nums: List of dice values rolled
        :return: [NONE]
        """
        for i, num in enumerate(nums):
            x = int(self.screen.get_width() * 0.94)
            y = int(self.screen.get_height() * (0.93 - i * 0.06))
            self.screen.blit(self.dice_dict["w"][num], (x, y))

    def draw_dice_r(self, nums):
        """
        Draws the red dice images on the screen based on the rolls provided in `nums`.
        It positions each die image on the screen
        :param nums: List of dice values rolled
        :return: [NONE]
        """
        for i, num in enumerate(nums):
            x = int(self.screen.get_width() * 0.91)
            y = int(self.screen.get_height() * (0.93 - i * 0.06))
            self.screen.blit(self.dice_dict["r"][num], (x, y))

    def create_dice(self):
        """
        Prepares and returns a dictionary mapping each die face value (1 through 6) to its corresponding scaled image.
        :return: dice_dict (Dictionary mapping die face values to images)
        """
        size = int(self.screen.get_height() * 0.04)
        dice_w = [
            pygame.transform.scale(die_img, (size, size)) for die_img in self.dice_w
        ]
        dice_r = [
            pygame.transform.scale(die_img, (size, size)) for die_img in self.dice_r
        ]
        dice_dict = {"w": {}, "r": {}}
        for i, (die_w, die_r) in enumerate(zip(dice_w, dice_r)):
            dice_dict["w"][i + 1] = die_w
            dice_dict["r"][i + 1] = die_r
        return dice_dict

# Finished
