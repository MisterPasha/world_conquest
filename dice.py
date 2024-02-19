import pygame
import random

pygame.init()


class Dice:
    def __init__(self):
        self.value = 0

    def set_value(self):
        self.value = random.randint(1, 7)

    def get_value(self):
        return self.value

    def animation(self):
        print("Does animation")