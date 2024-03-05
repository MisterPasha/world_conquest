import pygame
from main_menu import draw_text

pygame.init()


# Super Class for Human and AI agent
# Only holds methods and attributes that both Human and AI players will have in common
class Player:
    def __init__(self, screen, profile_img, color, color_str):
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

    # Adds troops that need to be placed
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
        draw_text(self.screen, f"troops: {self.troops_holds}", int(self.size[0] * 0.45), (0, 0, 0),
                  int(self.pos[0] * 0.92), int(self.pos[1] + 10))
        draw_text(self.screen, f"available: {self.troops_available}", int(self.size[0] * 0.45), (0, 0, 0),
                  int(self.pos[0] * 0.92), int(self.pos[1] + 30))

    def get_color(self):
        return self.color

    def get_color_name(self):
        return self.color_str

    def add_country(self, country):
        self.countries.append(country)

    def remove_country(self, country):
        print("Finish me =)")


class Human(Player):
    def __init__(self, screen, profile_img, color, color_str):
        super().__init__(screen, profile_img, color, color_str)

    def attack(self, country):
        print("attack", country)

    def roll_dice(self):
        return 0

    def choose_num_of_dice(self):
        return 0

class AI(Player):
    def __init__(self, screen, profile_img, color, color_str):
        super().__init__(screen, profile_img, color, color_str)

    def attack(self, country):
        print("attack", country)

    def roll_dice(self):
        return 0

    def choose_num_of_dice(self):
        return 0
