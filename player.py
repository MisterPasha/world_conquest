import pygame

pygame.init()


class Player:
    def __init__(self, profile_img, color, troops):
        self.profile = profile_img
        self.color = color
        self.troops = troops

    def attack(self, country):
        print("attack", country)

    def roll_dice(self):
        return 0

    def choose_num_of_dice(self):
        return 0


class Human(Player):
    def __init__(self, profile_img, color, troops):
        super().__init__(profile_img, color, troops)


class AI(Player):
    def __init__(self, profile_img, color, troops):
        super().__init__(profile_img, color, troops)