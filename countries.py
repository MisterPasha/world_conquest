import pygame

pygame.init()


class Country:
    def __init__(self, screen, image):
        self.owner = None
        self.troops = 0
        self.screen = screen
        self.image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
        self.color = (192, 192, 192)

    def set_owner(self, new_owner):
        self.owner = new_owner

    def add_troops(self, num_troops):
        self.troops += num_troops

    def remove_troops(self, num_troops):
        self.troops -= num_troops

    def draw(self):
        color = pygame.Color(self.color)
        color_image = self.fill_with_color(self.image, color)
        self.screen.blit(color_image, (0, 0))

    def fill_with_color(self, image, color):
        coloured_image = pygame.Surface(self.image.get_size())
        coloured_image.fill(color)

        final_image = image.copy()
        final_image.blit(coloured_image, (0, 0), special_flags=pygame.BLEND_MULT)
        return final_image

    def change_color(self, new_color):
        self.color = new_color


class Continent:
    def __init__(self, name):
        self.name = name
        self.list_of_countries = []

    def add_countries(self, countries):
        self.list_of_countries = countries
