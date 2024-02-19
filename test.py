from game import Game
import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame
from button import Button
from main_menu import MainMenu


class TestButton(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1280, 720))  # Mock display setup for Pygame

        self.original_image = pygame.Surface((100, 50))
        self.hover_image = pygame.Surface((100, 50))
        self.clicked_image = pygame.Surface((100, 50))
        self.unclicked_image = pygame.Surface((100, 50))

        self.pos = (50, 50)
        self.text = "Test Button"
        self.font_size = 30
        self.width = 100
        self.height = 50
        self.font = None
        self.action = Mock()

        # Create Button instance with mocks
        self.button = Button(self.original_image, self.hover_image, self.pos, self.text,
                             self.font_size, self.width, self.height, self.font, self.action)

    def test_check_click(self):
        # Mock the button's rect attribute to control the collidepoint method
        self.button.rect = Mock()
        self.button.rect.collidepoint.return_value = True
        mock_event = Mock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=self.pos)
        self.button.check_click(mock_event)
        self.action.assert_called_once()

    def test_change_image(self):
        new_image = pygame.Surface((100, 50))
        self.button.change_image(new_image)
        self.assertNotEqual(self.button.image, self.original_image)
        self.assertEqual(self.button.image.get_size(), (100, 50))

    def test_click(self):
        self.button.click(self.unclicked_image, self.clicked_image)
        self.assertTrue(self.button.clicked)
        self.button.click(self.unclicked_image, self.clicked_image)
        self.assertFalse(self.button.clicked)


class TestMainMenu(unittest.TestCase):
    def setUp(self):
        # Mock pygame functionalities used by MainMenu
        pygame.init()
        self.mock_screen = MagicMock()
        self.mock_screen.get_width.return_value = 1280
        self.mock_screen.get_height.return_value = 720

        # Patching pygame.transform.scale and other pygame functionalities
        self.patcher1 = patch('pygame.transform.scale', MagicMock(side_effect=lambda x, y: x))
        self.patcher2 = patch('pygame.font.Font', MagicMock())
        self.mock_scale = self.patcher1.start()
        self.mock_font = self.patcher2.start()

        # Initialize MainMenu with a mocked screen
        self.main_menu = MainMenu(self.mock_screen)
        with patch('pygame.transform.scale', MagicMock(side_effect=lambda x, y: x)), \
                patch('pygame.font.Font', MagicMock()):
            self.main_menu = MainMenu(self.mock_screen)
            # Assuming the MainMenu constructor or another method initializes player_slots
            # with a list of Button objects and that each Button object has a .change_image method
            self.main_menu.player_slots = [MagicMock() for _ in range(6)]  # Mock 6 player slots
            self.main_menu.player_images = [MagicMock() for _ in range(6)]  # Mock 6 player images

    def tearDown(self):
        # Stop all patches
        self.patcher1.stop()
        self.patcher2.stop()

    def test_initial_state(self):
        # Test initial state of MainMenu
        self.assertFalse(self.main_menu.opt_menu)
        self.assertFalse(self.main_menu.setting_menu)
        self.assertEqual(self.main_menu.state, 0)

    @patch('main_menu.Button.check_click')
    def test_check_clicks_main_menu(self, mock_check_click):
        # Simulate a click event and verify main menu buttons handle it
        mock_event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1)
        self.main_menu.check_clicks(mock_event)
        # Assert that check_click was called for each main menu button
        for button in self.main_menu.main_menu_buttons:
            button.check_click.assert_called_with(mock_event)

    @patch('main_menu.Button.check_click')
    def test_check_clicks_new_game_menu(self, mock_check_click):
        # Simulate a click event in the new game menu
        mock_event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1)
        self.main_menu.set_opt_menu(True)  # Switch to new game menu
        self.main_menu.check_clicks(mock_event)
        # Assert that check_click was called for each new game menu button
        for button in self.main_menu.new_menu_buttons:
            button.check_click.assert_called_with(mock_event)

    def test_add_player(self):
        initial_players = self.main_menu.players
        self.main_menu.add_player()
        # Check if the number of players increased by 1
        self.assertEqual(self.main_menu.players, initial_players + 1)
        # Verify the change_image method was called for the new player's slot
        self.main_menu.player_slots[initial_players].change_image.assert_called_once_with(
            self.main_menu.player_images[initial_players])


if __name__ == '__main__':
    unittest.main()