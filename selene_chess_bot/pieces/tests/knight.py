import unittest

from core.testing import print_starting, print_success

from board import Board

from pieces import Knight

from pieces.utilites import PieceColor, PieceName


class TestKnight(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board.create_empty_board()
        self.knight = self.add_knight_to_board()

    def tearDown(self) -> None:
        self.board.clean_board()
        self.knight = self.add_knight_to_board()
        return super().tearDown()

    def add_knight_to_board(self, row: int = 4, column: int = 4) -> Knight:
        return self.board.add_piece(
            piece=PieceName.KNIGHT,
            piece_color=PieceColor.WHITE,
            row=row,
            column=column
        )

    def test_calculate_legal_moves(self):
        print_starting()
        expected_moves = [
            (5, 6), (6, 5), (6, 3), (5, 2), (3, 2), (2, 3), (2, 5), (3, 6)
        ]
        self.assertEqual(
            self.knight.calculate_legal_moves(),
            expected_moves
        )
        print_success()

    def test_calculate_legal_moves_with_algebraic_notation(self):
        print_starting()
        expected_moves = [
            'f7', 'g6', 'g4', 'f3', 'd3', 'c4', 'c6', 'd7'
        ]
        self.assertEqual(
            sorted(
                self.knight.calculate_legal_moves(
                    show_in_algebraic_notation=True
                )
            ),
            sorted(expected_moves)
        )
        print_success()

    def test_enemy_piece_on_legal_move(self):
        print_starting()
        self.board.add_piece(
            piece=PieceName.PAWN,
            piece_color=PieceColor.BLACK,
            row=5,
            column=6
        )

        expected_moves = [
            (5, 6), (6, 5), (6, 3), (5, 2), (3, 2), (2, 3), (2, 5), (3, 6)
        ]
        self.assertEqual(
            self.knight.calculate_legal_moves(),
            expected_moves
        )

        print_success()

    def test_friendly_piece_on_legal_move(self):
        print_starting()
        self.board.add_piece(
            piece=PieceName.PAWN,
            piece_color=PieceColor.WHITE,
            row=5,
            column=6
        )

        expected_moves = [
            (6, 5), (6, 3), (5, 2), (3, 2), (2, 3), (2, 5), (3, 6)
        ]
        self.assertEqual(
            self.knight.calculate_legal_moves(),
            expected_moves
        )

        print_success()


if __name__ == '__main__':
    unittest.main()
