from game import Game
import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame  # Import the pygame library for game development
from button import Button  # Importing Button class from another module
from main_menu import MainMenu
from player import Player
from countries import Country
from map import Map


# class TestButton(unittest.TestCase):
#    def setUp(self):
#        pygame.init()
#        pygame.display.set_mode((1280, 720))  # Mock display setup for Pygame
#
#        self.original_image = pygame.Surface((100, 50))
#        self.hover_image = pygame.Surface((100, 50))
#        self.clicked_image = pygame.Surface((100, 50))
#        self.unclicked_image = pygame.Surface((100, 50))
#
#        self.pos = (50, 50)
#        self.text = "Test Button"
#        self.font_size = 30
#        self.width = 100
#        self.height = 50
#        self.font = None
#        self.action = Mock()
#
#        # Create Button instance with mocks
#        self.button = Button(self.original_image, self.hover_image, self.pos, self.text,
#                             self.font_size, self.width, self.height, self.font, self.action)
#
#    def test_check_click(self):
#        # Mock the button's rect attribute to control the collidepoint method
#        self.button.rect = Mock()
#        self.button.rect.collidepoint.return_value = True
#        mock_event = Mock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=self.pos)
#        self.button.check_click(mock_event)
#        self.action.assert_called_once()
#
#    def test_change_image(self):
#        new_image = pygame.Surface((100, 50))
#        self.button.change_image(new_image)
#        self.assertNotEqual(self.button.image, self.original_image)
#        self.assertEqual(self.button.image.get_size(), (100, 50))
#
#    def test_click(self):
#        self.button.click(self.unclicked_image, self.clicked_image)
#        self.assertTrue(self.button.clicked)
#        self.button.click(self.unclicked_image, self.clicked_image)
#        self.assertFalse(self.button.clicked)
#
#
# class TestMainMenu(unittest.TestCase):
#    def setUp(self):
#        # Mock pygame functionalities used by MainMenu
#        pygame.init()
#        self.mock_screen = MagicMock()
#        self.mock_screen.get_width.return_value = 1280
#        self.mock_screen.get_height.return_value = 720
#
#        # Patching pygame.transform.scale and other pygame functionalities
#        self.patcher1 = patch('pygame.transform.scale', MagicMock(side_effect=lambda x, y: x))
#        self.patcher2 = patch('pygame.font.Font', MagicMock())
#        self.mock_scale = self.patcher1.start()
#        self.mock_font = self.patcher2.start()
#
#        # Initialize MainMenu with a mocked screen
#        self.main_menu = MainMenu(self.mock_screen)
#        with patch('pygame.transform.scale', MagicMock(side_effect=lambda x, y: x)), \
#                patch('pygame.font.Font', MagicMock()):
#            self.main_menu = MainMenu(self.mock_screen)
#            # Assuming the MainMenu constructor or another method initializes player_slots
#            # with a list of Button objects and that each Button object has a .change_image method
#            self.main_menu.player_slots = [MagicMock() for _ in range(6)]  # Mock 6 player slots
#            self.main_menu.player_images = [MagicMock() for _ in range(6)]  # Mock 6 player images
#
#    def tearDown(self):
#        # Stop all patches
#        self.patcher1.stop()
#        self.patcher2.stop()
#
#    def test_initial_state(self):
#        # Test initial state of MainMenu
#        self.assertFalse(self.main_menu.opt_menu)
#        self.assertFalse(self.main_menu.setting_menu)
#        self.assertEqual(self.main_menu.state, 0)
#
#    @patch('main_menu.Button.check_click')
#    def test_check_clicks_main_menu(self, mock_check_click):
#        # Simulate a click event and verify main menu buttons handle it
#        mock_event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1)
#        self.main_menu.check_clicks(mock_event)
#        # Assert that check_click was called for each main menu button
#        for button in self.main_menu.main_menu_buttons:
#            button.check_click.assert_called_with(mock_event)
#
#    @patch('main_menu.Button.check_click')
#    def test_check_clicks_new_game_menu(self, mock_check_click):
#        # Simulate a click event in the new game menu
#        mock_event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1)
#        self.main_menu.set_opt_menu(True)  # Switch to new game menu
#        self.main_menu.check_clicks(mock_event)
#        # Assert that check_click was called for each new game menu button
#        for button in self.main_menu.new_menu_buttons:
#            button.check_click.assert_called_with(mock_event)
#
#    def test_add_player(self):
#        initial_players = self.main_menu.players
#        self.main_menu.add_player()
#        # Check if the number of players increased by 1
#        self.assertEqual(self.main_menu.players, initial_players + 1)
#        # Verify the change_image method was called for the new player's slot
#        self.main_menu.player_slots[initial_players].change_image.assert_called_once_with(
#            self.main_menu.player_images[initial_players])
#
#
# class TestPlayer(unittest.TestCase):
#    def setUp(self):
#        pygame.init()
#        self.screen = pygame.display.set_mode((800, 600))
#        self.profile_img = pygame.Surface((50, 50))  # Mock profile image
#        self.color = (255, 0, 0)  # Red
#        self.color_str = "red"
#        self.player = Player(self.screen, self.profile_img, self.color, self.color_str)
#
#    def test_add_avail_troops(self):
#        self.assertEqual(self.player.troops_available, 0)
#        self.player.add_avail_troops(5)
#        self.assertEqual(self.player.troops_available, 5)
#
#    def test_remove_avail_troop(self):
#        self.player.add_avail_troops(3)
#        self.player.remove_avail_troop()
#        self.assertEqual(self.player.troops_available, 2)
#        self.assertEqual(self.player.troops_holds, 1)
#
#    def test_set_pos_size(self):
#        self.assertIsNone(self.player.pos)
#        self.assertIsNone(self.player.size)
#        self.player.set_pos_size(100, 100, 50, 50)
#        self.assertEqual(self.player.pos, (100, 100))
#        self.assertEqual(self.player.size, (50, 50))
#        self.assertIsNotNone(self.player.profile)
#
#
# class TestCountry(unittest.TestCase):
#    def setUp(self):
#        # Initialize pygame and create a mock screen
#        pygame.init()
#        self.screen = pygame.display.set_mode((800, 600))
#        self.image = pygame.Surface((50, 50))  # Mock country image
#        self.name = "Test land"
#        # Patch the pygame and custom methods/classes used in Country
#        self.mock_button = Mock()
#        with patch('button.Button', return_value=self.mock_button):
#            self.country = Country(self.screen, self.image, self.name)
#
#    def test_get_name(self):
#        self.assertEqual(self.country.get_name(), "Test land")
#
#    @patch('player.pygame.image.load')
#    def test_set_owner(self, mock_load):
#        mock_owner = Mock()
#        mock_owner.get_color.return_value = (100, 100, 100)
#        self.country.set_owner(mock_owner)
#        self.assertEqual(self.country.owner, mock_owner)
#        self.assertEqual(self.country.color, (100, 100, 100))
#        # Ensure the methods to modify the image and button were called
#        mock_owner.get_color.assert_called_once()
#
#    def test_add_remove_troops(self):
#        self.assertEqual(self.country.troops, 0)
#        self.country.add_troops(5)
#        self.assertEqual(self.country.troops, 5)
#        self.country.remove_troops(3)
#        self.assertEqual(self.country.troops, 2)


class TestMap(unittest.TestCase):
    def setUp(self):
        """

        :return:
        """
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        # Mocking images and other Pygame objects that are used within the Map class
        self.mock_map_img = pygame.Surface((50, 50))
        self.mock_plate_img = pygame.Surface((50, 50))
        with patch("map.map_img", self.mock_map_img), patch(
                "map.plate_img", self.mock_plate_img
        ):
            self.map = Map(self.screen)

    def test_draw(self):
        """
        Test draw method. This test checks if the method can be called without errors.
        Actual drawing to the screen cannot be easily tested in a unit test.
        :return:
        """
        with patch.object(self.map, "draw_dice_plate") as mock_draw_plate, patch.object(
                self.map, "draw_turn_indicator"
        ) as mock_draw_turn_indicator:
            self.map.draw()
            mock_draw_plate.assert_called_once()
            mock_draw_turn_indicator.assert_called_once()

    def test_set_state(self):
        """

        :return:
        """
        self.assertIsNone(self.map.get_state())
        self.map.set_state("NEW_STATE")
        self.assertEqual(self.map.get_state(), "NEW_STATE")

    def test_set_players_and_ai(self):
        """

        :return:
        """
        self.assertEqual(self.map.players, 0)
        self.assertEqual(self.map.AI_players, 0)
        self.map.set_players_and_ai(2, 1)
        self.assertEqual(self.map.players, 2)
        self.assertEqual(self.map.AI_players, 1)

    def test_change_turn(self):
        """

        :return:
        """
        self.assertEqual(self.map.current_turn, 0)
        self.map.change_turn(1)
        self.assertEqual(self.map.current_turn, 1)


# ....
if __name__ == "__main__":
    unittest.main()
