import pygame
from main_menu import MainMenu

pygame.init()


class Game:
    # Game States
    EXIT = -1
    MAIN_MENU = 0
    GAMEPLAY_1 = 1  # 3-6 players game
    GAMEPLAY_2 = 2  # 2 players game

    def __init__(self, screen, clock, window_size):
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        # self.center = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.running = True
        # set initial state
        self.game_state = self.MAIN_MENU
        # Set initial numbers of players
        self.players = 0
        self.AI_agents = 0
        self.main_menu = MainMenu(self.screen)

    def run(self):
        while self.running:
            self.events()
            self.draw()
            self.check_state()
            self.clock.tick(60)
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.game_state == self.MAIN_MENU:
                self.main_menu.check_clicks(event)
            elif self.game_state == self.EXIT:
                self.running = False

    def draw(self):
        if self.game_state == self.MAIN_MENU:
            self.main_menu.draw()

    def check_state(self):
        if self.main_menu.get_state() == self.MAIN_MENU:
            self.game_state = self.MAIN_MENU
        elif self.main_menu.get_state() == self.EXIT:
            self.game_state = self.EXIT
