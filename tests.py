import unittest
from GessGame import Footprint, GessGame


class TestFootprintBasics(unittest.TestCase):
    """Tests basic functionality of the footprint class."""

    def test_footprint(self):
        """Tests footprint name."""
        test_foot = Footprint('b5')
        self.assertEqual(str(test_foot), 'b5')

    def test_footprint_center(self):
        """Tests accurate footprint center location."""
        test_foot = Footprint('b5')
        center = test_foot.get_center_coordinates()
        self.assertEqual(center, [15, 1])

    def test_footprint_footprint(self):
        """Tests accurate locations of the 9 squares of the footprint."""
        test_foot = Footprint('f17')
        footprint_coordinates = test_foot.get_footprint_coordinates()
        self.assertEqual(footprint_coordinates,[[3, 5], [2, 4], [3, 4], [4, 4], [4, 5], [2, 5], [2, 6], [3, 6], [4, 6]])


class TestGameBasics(unittest.TestCase):
    """Tests basic functionality of GessGame class."""

    def test_game_start_state(self):
        """Tests game state at the start of a game."""
        test_game = GessGame()
        state = test_game.get_game_state()
        self.assertEqual(state, "UNFINISHED")

    def test_game_resign(self):
        """Tests game resign functionality."""
        test_game = GessGame()
        test_game.resign_game()
        self.assertEqual(test_game.get_game_state(), "WHITE_WON")

    def test_invalid_user_input(self):
        """Tests error handling for user entering coordinates not on the board."""
        game = GessGame()
        game.make_move('x6', 'b5')
        self.assertRaises(KeyError)


class TestPieceMovement(unittest.TestCase):
    """Deals with movement of pieces/footprints on the board."""

    def test_spaces_allowed(self):
        """Tests number of spaces of movement allowed."""
        game = GessGame()
        result = game.make_move('c5', 'f9')
        self.assertFalse(result)

    # Test movement of directions for validity for each cardinal direction using start/destination points.
    def test_northwest_invalid(self):
        game = GessGame()
        result = game.make_move('c3', 'b4')
        self.assertFalse(result)

    def test_northwest_invalid2(self):
        game = GessGame()
        result = game.make_move('s3', 'q5')
        self.assertFalse(result)

    def test_northwest_valid(self):
        game = GessGame()
        result = game.make_move('f3', 'e4')
        self.assertTrue(result)

    def test_northwest_valid2(self):
        game = GessGame()
        result = game.make_move('s6', 'q8')
        self.assertTrue(result)

    def test_west_valid(self):
        game = GessGame()
        result = game.make_move('g7', 'e7')
        self.assertTrue(result)

    def test_west_valid2(self):
        game = GessGame()
        result = game.make_move('d4', 'c4')
        self.assertTrue(result)

    def test_west_invalid(self):
        game = GessGame()
        result = game.make_move('d4', 'b4')
        self.assertFalse(result)

    def test_north_valid(self):
        game = GessGame()
        result = game.make_move('i3', 'i5')
        self.assertTrue(result)

    def test_north_valid2(self):
        game = GessGame()
        result = game.make_move('r6', 'r8')
        self.assertTrue(result)

    def test_north_invalid(self):
        game = GessGame()
        result = game.make_move('i2', 'i4')
        self.assertFalse(result)

    def test_northeast_valid(self):
        game = GessGame()
        result = game.make_move('m3', 'n4')
        self.assertTrue(result)

    def test_northeast_valid2(self):
        game = GessGame()
        result = game.make_move('h6', 'k9')
        self.assertTrue(result)

    def test_northeast_invalid(self):
        game = GessGame()
        result = game.make_move('c3', 'd4')
        self.assertFalse(result)

    def test_southeast_valid(self):
        game = GessGame()
        result = game.make_move('b8', 'd6')
        self.assertTrue(result)

    def test_southeast_valid2(self):
        game = GessGame()
        result = game.make_move('k8', 'm6')
        self.assertTrue(result)

    def test_southeast_invalid(self):
        game = GessGame()
        result = game.make_move('c4', 'e2')
        self.assertFalse(result)

    def test_southwest_valid(self):
        game = GessGame()
        result = game.make_move('g8', 'e6')
        self.assertTrue(result)

    def test_southwest_valid2(self):
        game = GessGame()
        result = game.make_move('s3', 'r2')
        self.assertTrue(result)

    def test_southwest_invalid(self):
        game = GessGame()
        result = game.make_move('l4', 'j2')
        self.assertFalse(result)

    def test_south_valid(self):
        game = GessGame()
        result = game.make_move('c8', 'c6')
        self.assertTrue(result)

    def test_south_valid2(self):
        game = GessGame()
        result = game.make_move('r3', 'r2')
        self.assertTrue(result)

    def test_south_invalid(self):
        game = GessGame()
        result = game.make_move('f7', 'f5')
        self.assertFalse(result)

    def test_east_valid(self):
        game = GessGame()
        result = game.make_move('q3', 'r3')
        self.assertTrue(result)

    def test_east_valid2(self):
        game = GessGame()
        result = game.make_move('k7', 'm7')
        self.assertTrue(result)

    def test_east_invalid(self):
        game = GessGame()
        result = game.make_move('h3', 'k3')
        self.assertFalse(result)


class TestMultipleMoves(unittest.TestCase):
    """Tests multiple moves for correct functionality/game state."""

    def test_unfinished1(self):
        game = GessGame()
        game.alter_board_display(" ")
        game.make_move('c3', 'c6')
        game.make_move('c15', 'c12')
        self.assertEqual(game.get_game_state(), "UNFINISHED")

    def test_current_player(self):
        game = GessGame()
        game.alter_board_display(" ")
        game.make_move('c3', 'c6')
        self.assertEqual(game.get_current_player(), "WHITE")

    def test_waiting_player(self):
        game = GessGame()
        game.alter_board_display(" ")
        game.make_move('c3', 'c6')
        self.assertEqual(game.get_waiting_player(), "BLACK")


if __name__ == '__main__':
    unittest.main(exit=False)