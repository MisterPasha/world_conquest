import pygame

pygame.init()


class Player:
    def __init__(self, screen, profile_img, color):
        self.screen = screen
        self.profile = profile_img
        self.color = color
        self.troops = 0
        self.cards = []
        self.pos = None
        self.size = None

    def attack(self, country):
        print("attack", country)

    def roll_dice(self):
        return 0

    def choose_num_of_dice(self):
        return 0

    # Set Position and size of the profile image
    def set_pos_size(self, x, y, width, height):
        self.pos = (x, y)
        self.size = (width, height)
        self.profile = pygame.transform.scale(self.profile, self.size)

    # Draws profiles on the map
    def draw_profile(self):
        self.screen.blit(self.profile, self.pos)


class Human(Player):
    def __init__(self, screen, profile_img, color):
        super().__init__(screen, profile_img, color)

    def draw_profile(self):
        self.screen.blit(self.profile, self.pos)


class AI(Player):
    def __init__(self, screen, profile_img, color):
        super().__init__(screen, profile_img, color)
