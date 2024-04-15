import pygame  # Import the pygame library for game development
from button import Button  # Importing Button class from another module
import numpy as np  # Importing numpy for array manipulation

# Initialize pygame
pygame.init()


def draw_text(
    # Parameters for the function
    screen,
    text,
    size,
    color,
    x,
    y,
    font=None,
):
    """
    Draw text on the screen
    :param screen: Pygame screen surface
    :param text: Text to display
    :param size: Font size
    :param color: Color of the text
    :param x: X-coordinate of the text
    :param y: Y-coordinate of the text
    :param font: Font to use
    :return: [NONE]
    """
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def draw_text2(screen, text, size, color, x, y, font=None):
    """
    Draw text on the screen with line breaks on spaces if the text exceeds a certain width.
    :param screen: Pygame screen surface
    :param text: Text to display
    :param size: Font size
    :param color: Color of the text
    :param x: Initial X-coordinate of the text
    :param y: Initial Y-coordinate of the text
    :param font: Font to use
    :return: [NONE]
    """
    max_line_width = 10
    font = pygame.font.Font(font, size)
    words = text.split(' ')
    line = ''
    for word in words:
        # Check if adding the next word exceeds the line width
        test_line = line + word + ' '
        test_surface = font.render(test_line, True, color)

        if test_surface.get_width() > max_line_width:
            # If the line is too wide, draw the current line and start a new one
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x, y)
            screen.blit(text_surface, text_rect)
            # Move to the next line
            y += text_surface.get_height()
            line = word + ' '
        else:
            line = test_line

    # Draw the last line
    text_surface = font.render(line, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


class MainMenu:
    # All images
    background_image = pygame.image.load("images\\background_main_high.png")
    button_image = pygame.image.load("images\\button_high.png")
    button_hover_image = pygame.image.load("images\\button_hover.png")
    logo_image = pygame.image.load("images\\logo.png")
    new_game_paper = pygame.image.load("images\\new_game_paper_resized.png")
    button_paper_image = pygame.image.load("images\\button_paper.png")
    button_paper_hover_image = pygame.image.load("images\\button_paper_hover.png")
    player_slot_image = pygame.image.load("images\\player_slot.png")
    player_images = [
        # Player images
        pygame.image.load("images\\player_1.png"),
        pygame.image.load("images\\player_2.png"),
        pygame.image.load("images\\player_3.png"),
        pygame.image.load("images\\player_4.png"),
        pygame.image.load("images\\player_5.png"),
        pygame.image.load("images\\player_6.png"),
    ]
    robot_image = pygame.image.load("images\\robot.png")
    human_image = pygame.image.load("images\\human.png")
    P_or_AI_button = pygame.image.load("images\\choose_P_AI_button.png")
    P_or_AI_button_clicked = pygame.image.load("images\\choose_P_AI_button_clicked.png")
    font1 = "fonts\\font1.ttf"

    def __init__(self, screen):
        """
        Initialize the main menu
        :param screen: Pygame screen surface
        """
        self.screen = screen
        self.opt_menu = False
        self.setting_menu = False
        self.faq_menu = False
        self.state = 0
        self.players = 0
        self.AI_agents = 0
        self.player_types = []

        # Load images and scale them accordingly
        self.background_image = pygame.transform.scale(
            self.background_image, (screen.get_width(), screen.get_height())
        )
        self.logo_image = pygame.transform.scale(
            self.logo_image,
            (int(screen.get_width() * 0.25), int(screen.get_width() * 0.2)),
        )
        self.new_game_paper = pygame.transform.scale(
            self.new_game_paper,
            (int(screen.get_width() * 0.4), int(screen.get_height() * 0.9)),
        )

        self.center_x, self.center_y = screen.get_width() / 2, screen.get_height() / 2

        self.human_image = pygame.transform.scale(
            self.human_image, (int(self.center_x * 0.055), int(self.center_x * 0.055))
        )
        self.robot_image = pygame.transform.scale(
            self.robot_image, (int(self.center_x * 0.055), int(self.center_x * 0.055))
        )

        # Initialize various attributes and elements of the menu
        self.player_slots = self.create_player_slots()
        self.small_buttons = self.create_small_buttons()
        self.main_menu_buttons = self.create_main_menu_buttons()
        self.new_menu_buttons = self.create_new_game_menu_buttons()
        self.faq_menu_buttons = self.create_faq_menu_buttons()

        self.secret_mission_mode = False

    def draw(self):
        """
        Draw the main menu on the screen
        :return: [NONE]
        """
        # Draw background, logo, buttons, etc
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(
            self.logo_image, (int(self.center_x * 1.5), int(self.center_y * 0.08))
        )
        if not self.opt_menu:
            for button in self.main_menu_buttons:
                button.draw(self.screen)
        self.draw_opt_menu()
        if self.faq_menu:
            self.draw_faq_menu()

    def draw_opt_menu(self):
        """
        Draw the options (new game) menu on the screen
        :return: [NONE]
        """
        # Draw background, buttons, player slots, etc.
        if self.opt_menu:
            self.screen.blit(
                self.new_game_paper,
                (int(self.center_x * 0.08), int(self.center_y * 0.12)),
            )
            draw_text(
                self.screen,
                "Players",
                int(self.center_y * 0.14),
                (0, 0, 0),
                int(self.center_x * 0.14),
                int(self.center_y * 0.18),
                font=self.font1,
            )
            draw_text(
                self.screen,
                "Mission Cards",
                int(self.center_y * 0.08),
                (0, 0, 0),
                int(self.center_x * 0.48),
                int(self.center_y * 0.42),
                font=self.font1,
            )
            for slot in self.player_slots:
                slot.draw(self.screen)
                self.draw_icon(slot)
            for button in self.new_menu_buttons:
                button.draw(self.screen)
            for i in range(0, (self.players + self.AI_agents)):
                self.small_buttons[i].draw(self.screen)
                self.small_buttons[i + 6].draw(self.screen)

    def draw_faq_menu(self):
        """
        Draw the FAQ menu on the screen
        :return: [NONE]
        """
        self.screen.blit(
            self.new_game_paper,
            (int(self.center_x * 0.08), int(self.center_y * 0.12)),
        )
        draw_text(
            self.screen,
            "FAQ",
            int(self.center_y * 0.17),
            (0, 0, 0),
            int(self.center_x * 0.14),
            int(self.center_y * 0.18),
            font=self.font1,
        )
        for button in self.faq_menu_buttons:
            button.draw(self.screen)

    def check_clicks(self, event):
        """
        Check for mouse clicks on buttons in the menu
        :param event: Pygame event object
        :return: [NONE]
        """
        # Check for clicks on buttons based on the menu state
        if not self.opt_menu:
            for button in self.main_menu_buttons:
                button.check_click(event)
            for button in self.faq_menu_buttons:
                button.check_click(event)
        else:
            for button in self.new_menu_buttons:
                button.check_click(event)
            for i in range(0, (self.players + self.AI_agents)):
                self.small_buttons[i].check_click(event)
                self.small_buttons[i + 6].check_click(event)

    def draw_icon(self, slot):
        """
        Draw icons (Human and AI) beside a player slot
        :param slot: Player slot Button object
        :return: [NONE]
        """
        self.screen.blit(
            self.human_image,
            (int(slot.x + slot.image.get_width() + self.center_x * 0.05), int(slot.y)),
        )
        self.screen.blit(
            self.robot_image,
            (
                int(slot.x + slot.image.get_width() + self.center_x * 0.05),
                int(slot.y + self.center_x * 0.06),
            ),
        )

    def add_player_type(self, type_):
        """
        Adds a player type
        :param type_: The type of player to add
        :return: [NONE]
        """
        self.player_types.append(type_)

    def set_opt_menu(self, state):
        """
        Set the state of the options (for new game) menu
        :param state: Boolean indicating whether the menu should be displayed or not
        :return: [NONE]
        """
        self.opt_menu = state
        self.players = 0
        self.AI_agents = 0
        self.player_types = []
        for slot in self.player_slots:
            slot.change_image(self.player_slot_image)

    def set_setting_menu(self, state):
        """
        Sets the state of the setting menu
        :param state: Boolean indicating whether the menu should be displayed or not
        :return: [NONE]
        """
        self.setting_menu = state

    def set_faq_menu(self, state):
        """
        Sets the state of the FAQ menu
        :param state: Boolean indicating whether the menu should be displayed or not
        :return: [NONE]
        """
        self.faq_menu = state

    def change_state(self, new_state):
        """
        Changes the state of the game
        :param new_state: The new state to be set
        :return: [NONE]
        """
        if new_state == 1:
            if self.players + self.AI_agents == 2:
                self.state = 2
            elif self.players + self.AI_agents > 2:
                self.state = 1
        else:
            self.state = new_state

    def get_state(self):
        """
        Get the current state of the game
        :return: The current state
        """
        return self.state

    def get_num_players(self):
        """
        Get the number of human players in the game
        :return: The number of human players
        """
        return self.players

    def get_num_ai_players(self):
        """
        Get the number of AI players in the game
        :return: The number of AI players
        """
        return self.AI_agents

    def get_player_types(self):
        """
        :return: self.player_types: list
        """
        return self.player_types

    def add_player(self):
        """
        Add a player to the game if the total number of players (human and AI) is less than 6
        :return: [NONE]
        """
        if (self.players + self.AI_agents) < 6:
            self.players += 1
            self.add_player_type("human")
            self.player_slots[(self.players + self.AI_agents) - 1].change_image(
                self.player_images[(self.players + self.AI_agents) - 1]
            )

    def remove_player(self):
        """
        Remove a player from the game
        :return: [NONE]
        """
        if (self.players + self.AI_agents) > 0:

            self.player_slots[(self.players + self.AI_agents) - 1].change_image(
                self.player_slot_image
            )
            self.player_types.pop()
            if self.small_buttons[self.players + self.AI_agents - 1].clicked:
                self.players -= 1
            elif self.small_buttons[self.players + self.AI_agents + 5].clicked:
                self.AI_agents -= 1

                self.small_buttons[self.players + self.AI_agents + 6].click(
                    self.P_or_AI_button, self.P_or_AI_button_clicked
                )
                self.small_buttons[self.players + self.AI_agents].click(
                    self.P_or_AI_button, self.P_or_AI_button_clicked
                )

    def create_main_menu_buttons(self):
        """
        Create buttons for the main menu
        :return: A list of main menu buttons
        """
        play = Button(
            self.button_image,
            self.button_hover_image,
            (int(self.center_x * 0.2), int(self.center_y * 0.5)),
            "Play",
            int(self.center_y * 0.12),
            int(self.center_x * 0.35),
            int(self.center_y * 0.2),
            font=self.font1,
            action=lambda: self.set_opt_menu(True),
        )
        settings = Button(
            self.button_image,
            self.button_hover_image,
            (int(self.center_x * 0.2), int(self.center_y * 0.8)),
            "Settings",
            int(self.center_y * 0.12),
            int(self.center_x * 0.35),
            int(self.center_y * 0.2),
            font=self.font1,
            action=lambda: self.set_setting_menu(True),
        )
        FAQ = Button(
            self.button_image,
            self.button_hover_image,
            (int(self.center_x * 0.2), int(self.center_y * 1.1)),
            "FAQ",
            int(self.center_y * 0.12),
            int(self.center_x * 0.35),
            int(self.center_y * 0.2),
            font=self.font1,
            action=lambda: self.set_faq_menu(True),  # Use lambda to defer execution
        )
        quit_b = Button(
            self.button_image,
            self.button_hover_image,
            (int(self.center_x * 0.2), int(self.center_y * 1.4)),
            "Quit",
            int(self.center_y * 0.12),
            int(self.center_x * 0.35),
            int(self.center_y * 0.2),
            font=self.font1,
            action=lambda: self.change_state(-1),
        )
        return [play, settings, FAQ, quit_b]

    def create_new_game_menu_buttons(self):
        """
        Create buttons for the new game menu
        :return: A list of new game menu buttons
        """
        play = Button(
            self.button_image,
            self.button_hover_image,
            (int(self.center_x * 0.63), int(self.center_y * 1.7)),
            "Play",
            int(self.center_y * 0.08),
            int(self.center_x * 0.2),
            int(self.center_y * 0.15),
            font=self.font1,
            action=lambda: self.change_state(1),
        )
        back = Button(
            self.button_image,
            self.button_hover_image,
            (int(self.center_x * 0.13), int(self.center_y * 1.7)),
            "Back",
            int(self.center_y * 0.08),
            int(self.center_x * 0.2),
            int(self.center_y * 0.15),
            font=self.font1,
            action=lambda: self.set_opt_menu(False),
        )
        add = Button(
            self.button_paper_image,
            self.button_paper_hover_image,
            (int(self.center_x * 0.45), int(self.center_y * 0.23)),
            "Add",
            int(self.center_y * 0.06),
            int(self.center_x * 0.17),
            int(self.center_y * 0.12),
            font=self.font1,
            action=lambda: self.add_player(),
        )
        remove = Button(
            self.button_paper_image,
            self.button_paper_hover_image,
            (int(self.center_x * 0.65), int(self.center_y * 0.23)),
            "Remove",
            int(self.center_y * 0.06),
            int(self.center_x * 0.17),
            int(self.center_y * 0.12),
            font=self.font1,
            action=lambda: self.remove_player(),
        )
        secret_mission = Button(
            self.P_or_AI_button,
            self.P_or_AI_button,
            (int(self.center_x * 0.73), int(self.center_y * 0.435)),
            "",
            1,
            int(self.center_x * 0.035),
            int(self.center_x * 0.035),
            action=lambda: self.change_secret_mission_mode(),
            hover=False,
        )
        return [play, back, add, remove, secret_mission]

    def change_secret_mission_mode(self):
        """
        Toggles the secret mission mode
        :return: [NONE]
        """
        if self.players + self.AI_agents > 2:
            self.secret_mission_mode = not self.secret_mission_mode
            if self.secret_mission_mode:
                self.new_menu_buttons[4].change_image(self.P_or_AI_button_clicked)
            else:
                self.new_menu_buttons[4].change_image(self.P_or_AI_button)

    def create_faq_menu_buttons(self):
        """
        Create buttons for the FAQ menu
        :return: A list of FAQ menu buttons
        """
        back = Button(
            self.button_image,
            self.button_hover_image,
            (int(self.center_x * 0.13), int(self.center_y * 1.7)),
            "Back",
            int(self.center_y * 0.08),
            int(self.center_x * 0.2),
            int(self.center_y * 0.15),
            font=self.font1,
            action=lambda: self.set_faq_menu(False),
        )
        return [back]

    def create_player_slots(self):
        """
        Create player slots
        :return: A list of player slots
        """
        slots1 = [
            Button(
                self.player_slot_image,
                self.player_slot_image,
                (int(self.center_x * 0.2), int(self.center_y * i)),
                "",
                1,
                int(self.center_x * 0.12),
                int(self.center_x * 0.12),
                hover=False,
            )
            for i in np.arange(0.6, 1.5, 0.3)
        ]
        slots2 = [
            Button(
                self.player_slot_image,
                self.player_slot_image,
                (int(self.center_x * 0.53), int(self.center_y * i)),
                "",
                1,
                int(self.center_x * 0.12),
                int(self.center_x * 0.12),
                hover=False,
            )
            for i in np.arange(0.6, 1.5, 0.3)
        ]
        return slots1 + slots2

    def swap_to(self, button, player):
        """
        Swaps the button's functionality between human and AI selection
        :param button: The button to swap
        :param player: The player type to swap to (Human or AI)
        :return: The action function to execute the swap
        """

        def action():
            index = self.small_buttons.index(button)
            if player == "human" and button.clicked is False:
                button.click(self.P_or_AI_button, self.P_or_AI_button_clicked)
                self.small_buttons[index + 6].click(
                    self.P_or_AI_button, self.P_or_AI_button_clicked
                )
                self.players += 1
                self.AI_agents -= 1
                self.player_types[index] = "human"
            if player == "ai" and button.clicked is False:
                button.click(self.P_or_AI_button, self.P_or_AI_button_clicked)
                self.small_buttons[index - 6].click(
                    self.P_or_AI_button, self.P_or_AI_button_clicked
                )
                self.players -= 1
                self.AI_agents += 1
                self.player_types[index - 6] = "ai"

        return action

    def create_small_buttons(self):
        """
        Creates small buttons for player selection
        :return: A list of small buttons
        """
        buttons1 = []
        buttons2 = []
        for slot in self.player_slots:
            x = slot.x
            y = slot.y
            button1 = Button(
                self.P_or_AI_button,
                self.P_or_AI_button,
                (
                    int(x + slot.image.get_width() + self.center_x * 0.01),
                    int(y + self.center_x * 0.018),
                ),
                "",
                1,
                int(self.center_x * 0.035),
                int(self.center_x * 0.035),
                hover=False,
            )
            button2 = Button(
                self.P_or_AI_button,
                self.P_or_AI_button,
                (
                    int(x + slot.image.get_width() + self.center_x * 0.01),
                    int(y + self.center_x * 0.07),
                ),
                "",
                1,
                int(self.center_x * 0.035),
                int(self.center_x * 0.035),
                hover=False,
            )
            button1.action = self.swap_to(button1, "human")
            button2.action = self.swap_to(button2, "ai")
            buttons1.append(button1)
            buttons2.append(button2)
        for b in buttons1:
            b.change_image(self.P_or_AI_button_clicked)
            b.clicked = True
        return buttons1 + buttons2

# Finished
