from game import Game
import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame  # Import the pygame library for game development
from button import Button  # Importing Button class from another module
from main_menu import MainMenu
from player import Player
from countries import Country
from map import Map
from countries import Continent
from deck import Deck, Card


# class TestButton(unittest.TestCase):
#     def setUp(self):
#         pygame.init()
#         pygame.display.set_mode((1280, 720))  # Mock display setup for Pygame
#
#         self.original_image = pygame.Surface((100, 50))
#         self.hover_image = pygame.Surface((100, 50))
#         self.clicked_image = pygame.Surface((100, 50))
#         self.unclicked_image = pygame.Surface((100, 50))
#
#         self.pos = (50, 50)
#         self.text = "Test Button"
#         self.font_size = 30
#         self.width = 100
#         self.height = 50
#         self.font = None
#         self.action = Mock()
#
#         # Create Button instance with mocks
#         self.button = Button(
#             self.original_image,
#             self.hover_image,
#             self.pos,
#             self.text,
#             self.font_size,
#             self.width,
#             self.height,
#             self.font,
#             self.action,
#         )
#
#     def test_check_click(self):
#         # Mock the button's rect attribute to control the collidepoint method
#         self.button.rect = Mock()
#         self.button.rect.collidepoint.return_value = True
#         mock_event = Mock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=self.pos)
#         self.button.check_click(mock_event)
#         self.action.assert_called_once()
#
#     def test_change_image(self):
#         new_image = pygame.Surface((100, 50))
#         self.button.change_image(new_image)
#         self.assertNotEqual(self.button.image, self.original_image)
#         self.assertEqual(self.button.image.get_size(), (100, 50))
#
#     def test_click(self):
#         self.button.click(self.unclicked_image, self.clicked_image)
#         self.assertTrue(self.button.clicked)
#         self.button.click(self.unclicked_image, self.clicked_image)
#         self.assertFalse(self.button.clicked)
#
#
# class TestMainMenu(unittest.TestCase):
#     def setUp(self):
#         # Mock pygame functionalities used by MainMenu
#         pygame.init()
#         self.mock_screen = MagicMock()
#         self.mock_screen.get_width.return_value = 1280
#         self.mock_screen.get_height.return_value = 720
#
#         # Patching pygame.transform.scale and other pygame functionalities
#         self.patcher1 = patch(
#             "pygame.transform.scale", MagicMock(side_effect=lambda x, y: x)
#         )
#         self.patcher2 = patch("pygame.font.Font", MagicMock())
#         self.mock_scale = self.patcher1.start()
#         self.mock_font = self.patcher2.start()
#
#         # Initialize MainMenu with a mocked screen
#         self.main_menu = MainMenu(self.mock_screen)
#         with patch(
#             "pygame.transform.scale", MagicMock(side_effect=lambda x, y: x)
#         ), patch("pygame.font.Font", MagicMock()):
#             self.main_menu = MainMenu(self.mock_screen)
#             # Assuming the MainMenu constructor or another method initializes player_slots
#             # with a list of Button objects and that each Button object has a .change_image method
#             self.main_menu.player_slots = [
#                 MagicMock() for _ in range(6)
#             ]  # Mock 6 player slots
#             self.main_menu.player_images = [
#                 MagicMock() for _ in range(6)
#             ]  # Mock 6 player images
#
#     def tearDown(self):
#         # Stop all patches
#         self.patcher1.stop()
#         self.patcher2.stop()
#
#     def test_initial_state(self):
#         # Test initial state of MainMenu
#         self.assertFalse(self.main_menu.opt_menu)
#         self.assertFalse(self.main_menu.setting_menu)
#         self.assertEqual(self.main_menu.state, 0)
#
#     @patch("main_menu.Button.check_click")
#     def test_check_clicks_main_menu(self, mock_check_click):
#         # Simulate a click event and verify main menu buttons handle it
#         mock_event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1)
#         self.main_menu.check_clicks(mock_event)
#         # Assert that check_click was called for each main menu button
#         for button in self.main_menu.main_menu_buttons:
#             button.check_click.assert_called_with(mock_event)
#
#     @patch("main_menu.Button.check_click")
#     def test_check_clicks_new_game_menu(self, mock_check_click):
#         # Simulate a click event in the new game menu
#         mock_event = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1)
#         self.main_menu.set_opt_menu(True)  # Switch to new game menu
#         self.main_menu.check_clicks(mock_event)
#         # Assert that check_click was called for each new game menu button
#         for button in self.main_menu.new_menu_buttons:
#             button.check_click.assert_called_with(mock_event)
#
#     def test_add_player(self):
#         initial_players = self.main_menu.players
#         self.main_menu.add_player()
#         # Check if the number of players increased by 1
#         self.assertEqual(self.main_menu.players, initial_players + 1)
#         # Verify the change_image method was called for the new player's slot
#         self.main_menu.player_slots[
#             initial_players
#         ].change_image.assert_called_once_with(
#             self.main_menu.player_images[initial_players]
#         )
#
#
# class TestPlayer(unittest.TestCase):
#     def setUp(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((800, 600))
#         self.profile_img = pygame.Surface((50, 50))  # Mock profile image
#         self.color = (255, 0, 0)  # Red
#         self.color_str = "red"
#         self.player = Player(self.screen, self.profile_img, self.color, self.color_str)
#
#     def test_add_avail_troops(self):
#         self.assertEqual(self.player.troops_available, 0)
#         self.player.add_avail_troops(5)
#         self.assertEqual(self.player.troops_available, 5)
#
#     def test_remove_avail_troop(self):
#         self.player.add_avail_troops(3)
#         self.player.remove_avail_troop()
#         self.assertEqual(self.player.troops_available, 2)
#         self.assertEqual(self.player.troops_holds, 1)
#
#     def test_set_pos_size(self):
#         self.assertIsNone(self.player.pos)
#         self.assertIsNone(self.player.size)
#         self.player.set_pos_size(100, 100, 50, 50)
#         self.assertEqual(self.player.pos, (100, 100))
#         self.assertEqual(self.player.size, (50, 50))
#         self.assertIsNotNone(self.player.profile)
#
#
# class TestCountry(unittest.TestCase):
#     def setUp(self):
#         # Initialize pygame and create a mock screen
#         pygame.init()
#         self.screen = pygame.display.set_mode((800, 600))
#         self.image = pygame.Surface((50, 50))  # Mock country image
#         self.name = "Test land"
#         # Patch the pygame and custom methods/classes used in Country
#         self.mock_button = Mock()
#         with patch("button.Button", return_value=self.mock_button):
#             self.country = Country(self.screen, self.image, self.name)
#
#     def test_get_name(self):
#         self.assertEqual(self.country.get_name(), "Test land")
#
#     @patch("player.pygame.image.load")
#     def test_set_owner(self, mock_load):
#         mock_owner = Mock()
#         mock_owner.get_color.return_value = (100, 100, 100)
#         self.country.set_owner(mock_owner)
#         self.assertEqual(self.country.owner, mock_owner)
#         self.assertEqual(self.country.color, (100, 100, 100))
#         # Ensure the methods to modify the image and button were called
#         mock_owner.get_color.assert_called_once()
#
#     def test_add_remove_troops(self):
#         self.assertEqual(self.country.troops, 0)
#         self.country.add_troops(5)
#         self.assertEqual(self.country.troops, 5)
#         self.country.remove_troops(3)
#         self.assertEqual(self.country.troops, 2)


#class TestMap(unittest.TestCase):
#    def setUp(self):
#        """
#
#        :return:
#        """
#        pygame.init()
#        self.screen = pygame.display.set_mode((800, 600))
#        # Mocking images and other Pygame objects that are used within the Map class
#        self.mock_map_img = pygame.Surface((50, 50))
#        self.mock_plate_img = pygame.Surface((50, 50))
#        with patch("map.map_img", self.mock_map_img), patch(
#            "map.plate_img", self.mock_plate_img
#        ):
#            self.map = Map(self.screen)
#
#    def test_draw(self):
#        """
#        Test draw method. This test checks if the method can be called without errors.
#        Actual drawing to the screen cannot be easily tested in a unit test.
#        :return:
#        """
#        with patch.object(self.map, "draw_dice_plate") as mock_draw_plate, patch.object(
#            self.map, "draw_turn_indicator"
#        ) as mock_draw_turn_indicator:
#            self.map.draw()
#            mock_draw_plate.assert_called_once()
#            mock_draw_turn_indicator.assert_called_once()
#
#    def test_set_state(self):
#        """
#
#        :return:
#        """
#        self.assertIsNone(self.map.get_state())
#        self.map.set_state("NEW_STATE")
#        self.assertEqual(self.map.get_state(), "NEW_STATE")
#
#    def test_set_players_and_ai(self):
#        """
#
#        :return:
#        """
#        self.assertEqual(self.map.players, 0)
#        self.assertEqual(self.map.AI_players, 0)
#        self.map.set_players_and_ai(2, 1)
#        self.assertEqual(self.map.players, 2)
#        self.assertEqual(self.map.AI_players, 1)
#
#    def test_change_turn(self):
#        """
#
#        :return:
#        """
#        self.assertEqual(self.map.current_turn, 0)
#        self.map.change_turn(1)
#        self.assertEqual(self.map.current_turn, 1)
#
#
#class TestContinent(unittest.TestCase):
#    def setUp(self):
#        """
#        Setup method to create a continent object before each test.
#        """
#        self.continent = Continent("Europe")
#
#    def test_initialization(self):
#        """
#        Test the initialization of a Continent object.
#        """
#        self.assertEqual(self.continent.continent_name, "Europe", "Continent name should be Europe")
#        self.assertEqual(len(self.continent.countries_in_continent), 0, "Initial number of countries should be 0")
#
#    def test_add_country(self):
#        """
#        Test adding countries to the continent.
#        """
#        self.continent.add_country("Germany")
#        self.continent.add_country("France")
#        self.assertIn("Germany", self.continent.countries_in_continent, "Germany should be in the countries list")
#        self.assertIn("France", self.continent.countries_in_continent, "France should be in the countries list")
#        self.assertEqual(len(self.continent.countries_in_continent), 2, "There should be 2 countries in the continent")
#
#    def test_get_bonus(self):
#        """
#        Test retrieving the correct bonus value for the continent.
#        """
#        self.assertEqual(self.continent.get_bonus(), 5, "Bonus value for Europe should be 5")
#
#    def test_invalid_continent_bonus(self):
#        """
#        Test retrieving a bonus value for an invalid continent name.
#        """
#        invalid_continent = Continent("RafflesLand")
#        with self.assertRaises(KeyError):
#            invalid_continent.get_bonus()
#
#class TestDeck(unittest.TestCase):
#    def setUp(self):
#        """
#        Setup method to create a mocked Pygame screen object before each test.
#        """
#        pygame.init()
#        self.mock_screen = Mock(spec=pygame.Surface)
#        self.mock_screen.get_width.return_value = 80
#        self.mock_screen.get_height.return_value = 80
#
#    @patch("deck.pygame.transform.scale")
#    def test_create_cards(self, mock_scale):
#        """
#        Test the create_cards method to ensure cards are created correctly.
#        """
#        mock_scale.return_value = Mock(spec=pygame.Surface)  # Mock scaled images
#        mock_map = Mock()
#        mock_map.countries = [Mock(get_name=Mock(return_value=f"Country {i}")) for i in range(42)]
#        deck = Deck(self.mock_screen)
#        deck.create_cards(mock_map)
#        self.assertEqual(len(deck.cards), 44, "Deck should contain 44 cards")
#        infantry, cavalry, artillery, wild = 14, 14, 14, 2
#        self.assertEqual(sum(1 for card in deck.cards if card.army_type == "Infantry"), infantry,
#                         "Incorrect number of Infantry cards")
#        self.assertEqual(sum(1 for card in deck.cards if card.army_type == "Cavalry"), cavalry,
#                         "Incorrect number of Cavalry cards")
#        self.assertEqual(sum(1 for card in deck.cards if card.army_type == "Artillery"), artillery,
#                         "Incorrect number of Artillery cards")
#        self.assertEqual(sum(1 for card in deck.cards if card.army_type == "Wild"), wild,
#                         "Incorrect number of Wild cards")
#
#    @patch("deck.random.randint", return_value=0)
#    def test_get_card(self, mock_randint):
#        """
#        Test getting a card from the deck.
#        """
#        self.mock_screen = Mock(spec=pygame.Surface)
#        deck = Deck(self.mock_screen)
#        deck.cards = [Mock(spec=Card) for _ in range(10)]  # Mocking 10 cards
#        initial_deck_size = len(deck.cards)
#        card = deck.get_card()
#        self.assertIsInstance(card, Mock, "The returned object should be a card")
#        self.assertEqual(len(deck.cards), initial_deck_size - 1, "Deck size should decrease by 1")
#
class TestPlayer(unittest.TestCase):
    def setUp(self):
        """
        Setup method to create a Player object and mock dependencies before each test.
        """
        self.mock_screen = Mock()  # Mock the Pygame screen
        self.mock_screen.get_width.return_value = 800
        self.mock_screen.get_height.return_value = 800
        self.mock_profile_img = Mock()  # Mock the player's profile image
        self.color = (255, 255, 255)  # White
        self.color_str = "white"
        self.player = Player(self.mock_screen, self.mock_profile_img, self.color, self.color_str)

    @patch("player.pygame.image.load")
    @patch("player.pygame.transform.scale")
    def test_initialization(self, mock_scale, mock_load):
        """
        Test that a Player object initializes correctly.
        """
        mock_load.return_value = Mock()  # Mock the image load return value
        mock_scale.return_value = Mock()  # Mock the transform scale return value
        self.assertTrue(self.player.playing)
        self.assertEqual(self.player.troops_holds, 0)
        self.assertEqual(len(self.player.cards), 0)

    def test_add_card(self):
        """
        Test adding a card to the player's collection.
        """
        mock_card = Mock(spec=Card)
        self.player.add_card(mock_card)
        self.assertIn(mock_card, self.player.cards)

    def test_calculate_num_of_draft_troops(self):
        """
        Test calculating the number of draft troops.
        """
        # Test for less than 9 countries
        for i in range(1, 10):
            with self.subTest(i=i):
                self.player.countries = [Mock(spec=Country) for _ in range(i)]
                expected_troops = 3
                self.assertEqual(self.player.calculate_num_of_draft_troops(), expected_troops)

        # Test for more than 9 countries
        self.player.countries = [Mock(spec=Country) for _ in range(11)]
        expected_troops = 11 // 3
        self.assertEqual(self.player.calculate_num_of_draft_troops(), expected_troops)

    def test_have_set_of_cards(self):
        """
        Test checking if player has a set of cards.
        """
        # Setup cards for having a set
        infantry_card = Card(self.mock_screen, "Country1", "Infantry", None)
        cavalry_card = Card(self.mock_screen, "Country2", "Cavalry", None)
        artillery_card = Card(self.mock_screen, "Country3", "Artillery", None)
        self.player.cards = [infantry_card, cavalry_card, artillery_card]
        self.assertTrue(self.player.have_set_of_cards())

    def test_remove_set_cards(self):
        """
        Test removing a set of same type cards from the player's hand.
        """
        deck = Mock()
        deck.cards = []
        # Create three infantry cards and add them to the player's hand
        for _ in range(3):
            self.player.cards.append(Card(self.mock_screen, "Country", "Infantry", None))
        # Add a wild card as well
        self.player.cards.append(Card(self.mock_screen, "Wild", "Wild", None))

        self.player.remove_set_cards("Infantry", deck)
        # Check that the player's hand has 1 card and the deck received the cards
        self.assertEqual(len(self.player.cards), 1)
        self.assertEqual(len(deck.cards), 3)

    def test_remove_distinct_cards(self):
        deck = Mock()
        deck.cards = []
        # Add one of each type to the player's hand
        self.player.cards = [Card(self.mock_screen, "Country1", "Infantry", None),
                             Card(self.mock_screen, "Country2", "Cavalry", None),
                             Card(self.mock_screen, "Country3", "Artillery", None)]
        self.player.remove_distinct_cards(deck)
        # Check that the player's hand is empty and the deck received the cards
        self.assertEqual(len(self.player.cards), 0)
        self.assertEqual(len(deck.cards), 3)

    def test_sell_cards(self):
        """
        Test selling cards for troops.
        """
        deck = Mock()
        deck.cards = []
        # Add cards to ensure a set can be sold
        self.player.cards = [Card(self.mock_screen, "Country1", "Infantry", None) for _ in range(3)]
        initial_troops = self.player.troops_available
        nth_set = 1  # First set sold
        self.player.sell_cards(nth_set, deck)
        # Verify troops were added
        expected_troops = initial_troops + self.player.get_card_bonus(nth_set)
        self.assertEqual(self.player.troops_available, expected_troops)
        # Ensure cards were moved to deck
        self.assertEqual(len(deck.cards), 3)

    def test_get_card_bonus(self):
        """
        Test the calculation of troops from selling cards for the nth set.
        """
        # Test for a range of set numbers
        for nth_set in range(1, 10):
            expected_bonus = 0
            if nth_set < 6:
                expected_bonus = nth_set * 2 + 2
            elif nth_set == 6:
                expected_bonus = 12
            else:
                expected_bonus = (nth_set - 6) * 5 + 15

            self.assertEqual(self.player.get_card_bonus(nth_set), expected_bonus)


if __name__ == "__main__":
    unittest.main()

