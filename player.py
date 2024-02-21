import pygame

pygame.init()


class Player:
    def __init__(self, screen, profile_img, color):
        self.screen = screen
        self.profile = profile_img
        self.color = color
        self.troops_holds = 0
        self.troops_available = 0
        self.cards = []
        self.countries = []
        self.pos = None
        self.size = None

    def attack(self, country):
        print("attack", country)

    def roll_dice(self):
        return 0

    def choose_num_of_dice(self):
        return 0

    def add_avail_troops(self, num_of_troops):
        self.troops_available += num_of_troops

    # Set Position and size of the profile image
    def set_pos_size(self, x, y, width, height):
        self.pos = (x, y)
        self.size = (width, height)
        self.profile = pygame.transform.scale(self.profile, self.size)

    # Draws profiles on the map
    def draw_profile(self):
        self.screen.blit(self.profile, self.pos)

    def get_color(self):
        return self.color


class Human(Player):
    def __init__(self, screen, profile_img, color):
        super().__init__(screen, profile_img, color)

    def draw_profile(self):
        self.screen.blit(self.profile, self.pos)


class AI(Player):
    def __init__(self, screen, profile_img, color):
        super().__init__(screen, profile_img, color)
