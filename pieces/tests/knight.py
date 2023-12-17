import unittest
from knight import Knight

class TestKnight(unittest.TestCase):
    def setUp(self):
        self.board = MockBoard()  # You'll need to define this
        self.knight = Knight((4, 4), self.board)

    def test_calculate_legal_moves(self):
        # Test that the knight calculates legal moves correctly
        expected_moves = [
            (5, 6), (6, 5), (6, 3), (5, 2), (3, 2), (2, 3), (2, 5), (3, 6)
        ]
        self.assertEqual(
            self.knight.calculate_legal_moves(),
            expected_moves
        )

    def test_calculate_legal_moves_with_algebraic_notation(self):
        # Test that the knight calculates legal moves correctly and converts them to algebraic notation
        expected_moves = [
            'f7', 'g6', 'g4', 'f3', 'd3', 'c4', 'c6', 'd7'
        ]
        self.assertEqual(
            self.knight.calculate_legal_moves(show_in_algebraic_notation=True),
            expected_moves
        )

if __name__ == '__main__':
    unittest.main()