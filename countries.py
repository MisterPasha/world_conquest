import pygame

pygame.init()


class Country:
    def __init__(self):
        self.owner = None
        self.troops = 0

    def set_owner(self, new_owner):
        self.owner = new_owner

    def add_troops(self, num_troops):
        self.troops += num_troops

    def remove_troops(self, num_troops):
        self.troops -= num_troops


class Continent:
    def __init__(self, name):
        self.name = name
        self.list_of_countries = []

    def add_countries(self, countries):
        self.list_of_countries = countries