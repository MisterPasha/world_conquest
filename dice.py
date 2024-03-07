import pygame
import random
from main_menu import draw_text

pygame.init()


class Dice:
    # Loading dice face images.
    dice = [
        pygame.image.load("images\\die1.png"),
        pygame.image.load("images\\die2.png"),
        pygame.image.load("images\\die3.png"),
        pygame.image.load("images\\die4.png"),
        pygame.image.load("images\\die5.png"),
        pygame.image.load("images\\die6.png"),
    ]

    def __init__(self, screen):
        """
        Initialise DiceHandler in accordance to the screen
        + dictionary of dice images
        :param screen:
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
        :param nums:
        :param name:
        :return: Shows the correct die
        """
        draw_text(
            self.screen,
            f"{name} rolled a total of {sum(nums)}",
            int(self.screen.get_height() * 0.07),
            (133, 14, 12),
            int(self.screen.get_width() * 0.3),
            int(self.screen.get_height() * 0.7),
        )
        self.draw_dice(nums)

    def draw_dice(self, nums):
        """
        Draws the dice images on the screen based on the rolls provided in `nums`.
        It positions each die image on the screen
        :param nums:
        :return:
        """
        for i, num in enumerate(nums):
            x = int(self.screen.get_width() * 0.93)
            y = int(self.screen.get_height() * (0.9 - i * 0.07))
            self.screen.blit(self.dice_dict[num], (x, y))

    def create_dice(self):
        """
        Prepares and returns a dictionary mapping each die face value (1 through 6) to its corresponding scaled image.
        :return: dice_dict
        """
        dice_dict = {}
        size = int(self.screen.get_height() * 0.05)
        dice = [pygame.transform.scale(die_img, (size, size)) for die_img in self.dice]
        for i, die in enumerate(dice):
            dice_dict[i + 1] = die
        return dice_dict

# eh-hh was-sup doc -test push
