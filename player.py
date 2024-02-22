import pygame
from main_menu import draw_text

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

    def add_avail_troops(self, num_of_troops):
        self.troops_available += num_of_troops

    def remove_avail_troop(self):
        self.troops_available -= 1
        self.troops_holds += 1

    # Set Position and size of the profile image
    def set_pos_size(self, x, y, width, height):
        self.pos = (x, y)
        self.size = (width, height)
        self.profile = pygame.transform.scale(self.profile, self.size)

    # Draws profiles on the map
    def draw_profile(self):
        self.screen.blit(self.profile, self.pos)
        draw_text(self.screen, f"troops: {self.troops_holds}", int(self.size[0] * 0.4), (255, 255, 255),
                  int(self.pos[0] * 0.9), int(self.pos[1] + 10))
        draw_text(self.screen, f"available: {self.troops_available}", int(self.size[0] * 0.4), (255, 255, 255),
                  int(self.pos[0] * 0.9), int(self.pos[1] + 30))


    def get_color(self):
        return self.color


class Human(Player):
    def __init__(self, screen, profile_img, color):
        super().__init__(screen, profile_img, color)

    def attack(self, country):
        print("attack", country)

    def roll_dice(self):
        return 0

    def choose_num_of_dice(self):
        return 0


class AI(Player):
    def __init__(self, screen, profile_img, color):
        super().__init__(screen, profile_img, color)
