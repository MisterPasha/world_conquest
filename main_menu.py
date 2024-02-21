import pygame
from button import Button
import numpy as np

pygame.init()


# Draws text
def draw_text(screen, text, size, color, x, y, font=None, ):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


class MainMenu:
    # All necessary imports of images and fonts
    background_image = pygame.image.load("images\\background_main_high.png")
    button_image = pygame.image.load("images\\button_high.png")
    button_hover_image = pygame.image.load("images\\button_hover.png")
    logo_image = pygame.image.load("images\\logo.png")
    new_game_paper = pygame.image.load("images\\new_game_paper_resized.png")
    button_paper_image = pygame.image.load("images\\button_paper.png")
    button_paper_hover_image = pygame.image.load("images\\button_paper_hover.png")
    player_slot_image = pygame.image.load("images\\player_slot.png")
    player_images = [pygame.image.load("images\\player1.png"), pygame.image.load("images\\player2.png"),
                     pygame.image.load("images\\player3.png"), pygame.image.load("images\\player4.png"),
                     pygame.image.load("images\\player5.png"), pygame.image.load("images\\player6.png")]
    robot_image = pygame.image.load("images\\robot.png")
    human_image = pygame.image.load("images\\human.png")
    P_or_AI_button = pygame.image.load("images\\choose_P_AI_button.png")
    P_or_AI_button_clicked = pygame.image.load("images\\choose_P_AI_button_clicked.png")
    font1 = "fonts\\font1.ttf"

    def __init__(self, screen):
        self.screen = screen
        # Enable or disable new game menu
        self.opt_menu = False
        # Enable or disable setting menu
        self.setting_menu = False
        # current state
        self.state = 0
        # Number of players
        self.players = 0
        # Number of AI agents
        self.AI_agents = 0
        # Get middle pixel on x and y axis
        self.center_x, self.center_y = screen.get_width() / 2, screen.get_height() / 2
        # Rescale images
        self.background_image = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))
        self.logo_image = pygame.transform.scale(self.logo_image, (int(screen.get_width() * 0.3),
                                                                   int(screen.get_height() * 0.12)))
        self.new_game_paper = pygame.transform.scale(self.new_game_paper, (int(screen.get_width() * 0.4),
                                                                           int(screen.get_height() * 0.9)))
        self.human_image = pygame.transform.scale(self.human_image, (int(self.center_x * 0.055),
                                                                     int(self.center_x * 0.055)))
        self.robot_image = pygame.transform.scale(self.robot_image, (int(self.center_x * 0.055),
                                                                     int(self.center_x * 0.055)))
        # List of empty player slots
        self.player_slots = self.create_player_slots()
        # List of small Switch buttons
        self.small_buttons = self.create_small_buttons()
        # List of buttons for Main Menu
        self.main_menu_buttons = self.create_main_menu_buttons()
        # List of buttons for New Menu
        self.new_menu_buttons = self.create_new_game_menu_buttons()

    # Draws all elements for Main Menu and New Game Menu
    def draw(self):
        # Set background
        self.screen.blit(self.background_image, (0, 0))
        # Set Logo Image
        self.screen.blit(self.logo_image, (int(self.center_x * 1.3), int(self.center_y * 0.1)))
        # When new game menu is on - Do not draw Main Menu buttons
        if not self.opt_menu:
            for button in self.main_menu_buttons:
                button.draw(self.screen)
        self.draw_opt_menu()

    # Draws all elements necessary for New Game Menu
    def draw_opt_menu(self):
        if self.opt_menu:
            self.screen.blit(self.new_game_paper, (int(self.center_x * 0.08), int(self.center_y * 0.12)))
            draw_text(self.screen, "Players", int(self.center_y * 0.17), (0, 0, 0), int(self.center_x * 0.14),
                      int(self.center_y * 0.18), font=self.font1)
            for slot in self.player_slots:
                slot.draw(self.screen)
                self.draw_icon(slot)
            for button in self.new_menu_buttons:
                button.draw(self.screen)
            for i in range(0, (self.players + self.AI_agents)):
                self.small_buttons[i].draw(self.screen)
                self.small_buttons[i+6].draw(self.screen)

    # Check click for each button
    def check_clicks(self, event):
        if not self.opt_menu:
            for button in self.main_menu_buttons:
                button.check_click(event)
        else:
            for button in self.new_menu_buttons:
                button.check_click(event)
            for i in range(0, (self.players + self.AI_agents)):
                self.small_buttons[i].check_click(event)
                self.small_buttons[i+6].check_click(event)

    # Draw human and robot icons for switch buttons
    def draw_icon(self, slot):
        self.screen.blit(self.human_image, (int(slot.x + slot.image.get_width() + self.center_x * 0.05),
                                            int(slot.y)))
        self.screen.blit(self.robot_image, (int(slot.x + slot.image.get_width() + self.center_x * 0.05),
                                            int(slot.y + self.center_x * 0.06)))

    # Start Showing or Stop Showing New Game Menu
    def set_opt_menu(self, state):
        self.opt_menu = state
        # Refresh New Game Menu choices
        self.players = 0
        self.AI_agents = 0
        for slot in self.player_slots:
            slot.change_image(self.player_slot_image)

    # Start Showing or Stop Showing Setting Menu (NO SETTING MENU YET)
    def set_setting_menu(self, state):
        self.setting_menu = state

    # Change state of the game
    def change_state(self, new_state):
        if new_state == 1:
            if self.players + self.AI_agents == 2:
                self.state = 2
            elif self.players + self.AI_agents > 2:
                self.state = 1
        else:
            self.state = new_state

    # Return Current State
    def get_state(self):
        return self.state

    def get_num_players(self):
        return self.players

    def get_num_ai_players(self):
        return self.AI_agents

    # Adds a players and adds player profile image to the new game menu
    def add_player(self):
        if (self.players + self.AI_agents) < 6:
            self.players += 1
            self.player_slots[(self.players + self.AI_agents) - 1].change_image(
                self.player_images[(self.players + self.AI_agents) - 1])

    # Removes a player and makes last added player's profile an empty slot
    def remove_player(self):
        if (self.players + self.AI_agents) > 0:
            self.player_slots[(self.players + self.AI_agents) - 1].change_image(self.player_slot_image)
            if self.small_buttons[self.players + self.AI_agents - 1].clicked:
                self.players -= 1
            elif self.small_buttons[self.players + self.AI_agents + 5].clicked:
                self.AI_agents -= 1
                self.small_buttons[self.players + self.AI_agents + 6].click(self.P_or_AI_button,
                                                                            self.P_or_AI_button_clicked)
                self.small_buttons[self.players + self.AI_agents].click(self.P_or_AI_button,
                                                                        self.P_or_AI_button_clicked)

    # Initialise and return a list of all buttons for Main Menu
    def create_main_menu_buttons(self):
        play = Button(self.button_image, self.button_hover_image, (int(self.center_x * 0.2), int(self.center_y * 0.5)),
                      "Play", int(self.center_y * 0.12), int(self.center_x * 0.35), int(self.center_y * 0.2),
                      font=self.font1, action=lambda: self.set_opt_menu(True))
        settings = Button(self.button_image, self.button_hover_image, (int(self.center_x * 0.2),
                                                                       int(self.center_y * 0.8)), "Settings",
                          int(self.center_y * 0.12), int(self.center_x * 0.35), int(self.center_y * 0.2),
                          font=self.font1, action=lambda: self.set_setting_menu(True))
        quit_b = Button(self.button_image, self.button_hover_image, (int(self.center_x * 0.2),
                                                                     int(self.center_y * 1.1)), "Quit",
                        int(self.center_y * 0.12), int(self.center_x * 0.35), int(self.center_y * 0.2), font=self.font1,
                        action=lambda: self.change_state(-1))
        return [play, settings, quit_b]

    # Initialise and return a list of all buttons for New Game Menu
    def create_new_game_menu_buttons(self):
        play = Button(self.button_image, self.button_hover_image, (int(self.center_x * 0.63),
                                                                   int(self.center_y * 1.7)), "Play",
                      int(self.center_y * 0.08), int(self.center_x * 0.2), int(self.center_y * 0.15), font=self.font1,
                      action=lambda: self.change_state(1))
        back = Button(self.button_image, self.button_hover_image, (int(self.center_x * 0.13),
                                                                   int(self.center_y * 1.7)), "Back",
                      int(self.center_y * 0.08), int(self.center_x * 0.2), int(self.center_y * 0.15), font=self.font1,
                      action=lambda: self.set_opt_menu(False))
        add = Button(self.button_paper_image, self.button_paper_hover_image, (int(self.center_x * 0.45),
                                                                              int(self.center_y * 0.23)), "Add",
                     int(self.center_y * 0.06), int(self.center_x * 0.17), int(self.center_y * 0.12), font=self.font1,
                     action=lambda: self.add_player())
        remove = Button(self.button_paper_image, self.button_paper_hover_image, (int(self.center_x * 0.65),
                                                                                 int(self.center_y * 0.23)), "Remove",
                        int(self.center_y * 0.06), int(self.center_x * 0.17), int(self.center_y * 0.12),
                        font=self.font1, action=lambda: self.remove_player())
        return [play, back, add, remove]

    # Initialise and return a list of all empty player slots
    def create_player_slots(self):
        slots1 = [Button(self.player_slot_image, self.player_slot_image, (int(self.center_x * 0.2),
                                                                          int(self.center_y * i)), "",
                         1, int(self.center_x * 0.12), int(self.center_x * 0.12), hover=False)
                  for i in np.arange(0.6, 1.5, 0.3)]
        slots2 = [Button(self.player_slot_image, self.player_slot_image, (int(self.center_x * 0.53),
                                                                          int(self.center_y * i)), "",
                         1, int(self.center_x * 0.12), int(self.center_x * 0.12), hover=False)
                  for i in np.arange(0.6, 1.5, 0.3)]
        return slots1 + slots2

    # Specific trigger function for small Switch Buttons when choosing human or AI player
    def swap_to(self, button, player):
        def action():
            index = self.small_buttons.index(button)
            if player == "human" and button.clicked is False:
                button.click(self.P_or_AI_button, self.P_or_AI_button_clicked)
                self.small_buttons[index + 6].click(self.P_or_AI_button, self.P_or_AI_button_clicked)
                self.players += 1
                self.AI_agents -= 1
            if player == "ai" and button.clicked is False:
                button.click(self.P_or_AI_button, self.P_or_AI_button_clicked)
                self.small_buttons[index - 6].click(self.P_or_AI_button, self.P_or_AI_button_clicked)
                self.players -= 1
                self.AI_agents += 1
        return action

    # initialise and return a list of small Switch Buttons when choosing human or AI player
    def create_small_buttons(self):
        buttons1 = []
        buttons2 = []
        for slot in self.player_slots:
            x = slot.x
            y = slot.y
            button1 = Button(self.P_or_AI_button, self.P_or_AI_button,
                             (int(x + slot.image.get_width() + self.center_x * 0.01), int(y + self.center_x * 0.018)),
                             "", 1, int(self.center_x * 0.035), int(self.center_x * 0.035), hover=False)
            button2 = Button(self.P_or_AI_button, self.P_or_AI_button,
                             (int(x + slot.image.get_width() + self.center_x * 0.01), int(y + self.center_x * 0.07)),
                             "", 1, int(self.center_x * 0.035), int(self.center_x * 0.035), hover=False)
            button1.action = self.swap_to(button1, "human")
            button2.action = self.swap_to(button2, "ai")
            buttons1.append(button1)
            buttons2.append(button2)
        for b in buttons1:
            b.change_image(self.P_or_AI_button_clicked)
            b.clicked = True
        return buttons1 + buttons2
