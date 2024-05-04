# FILEPATH: /c:/Users/andre/Desktop/selene_chess/pieces/tests/queen.py
import unittest

from core.testing import print_starting, print_success

from board import Board

from pieces import Queen

from pieces.utilites import PieceColor, PieceName


class TestQueen(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board.create_empty_board()
        self.queen = self.add_queen_to_board()

    def tearDown(self) -> None:
        self.board.clean_board()
        self.queen = self.add_queen_to_board()
        return super().tearDown()

    def add_queen_to_board(self, row: int = 4, column: int = 4) -> Queen:
        return self.board.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.WHITE,
            row=row,
            column=column
        )

    def test_calculate_legal_moves(self):
        print_starting()
        expected_moves = [
            [4, 0], [4, 1], [4, 2], [4, 3], [4, 5], [4, 6], [4, 7],
            [0, 4], [1, 4], [2, 4], [3, 4], [5, 4], [6, 4], [7, 4],
            [0, 0], [1, 1], [2, 2], [3, 3], [5, 5], [6, 6], [7, 7],
            [1, 7], [2, 6], [3, 5], [5, 3], [6, 2], [7, 1]
        ]
        calculated_moves = self.queen.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()

    def test_calculate_legal_moves_with_algebraic_notation(self):
        print_starting()
        expected_moves = [
            'e1', 'e2', 'e3', 'e4', 'e6', 'e7', 'e8', 'a5', 'b5', 'c5',
            'd5', 'f5', 'g5', 'h5', 'a1', 'b2', 'c3', 'd4', 'f6', 'g7',
            'h8', 'b8', 'c7', 'd6', 'f4', 'g3', 'h2'
        ]
        self.assertEqual(
            sorted(
                self.queen.calculate_legal_moves(
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
            [4, 0], [4, 1], [4, 2], [4, 3], [4, 5], [4, 6], [4, 7],
            [0, 4], [1, 4], [2, 4], [3, 4], [5, 4], [6, 4], [7, 4],
            [0, 0], [1, 1], [2, 2], [3, 3], [5, 5], [6, 6], [7, 7],
            [1, 7], [2, 6], [3, 5], [5, 3], [6, 2], [7, 1]
        ]
        calculated_moves = self.queen.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
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
            [4, 0], [4, 1], [4, 2], [4, 3], [4, 5], [4, 6], [4, 7],
            [0, 4], [1, 4], [2, 4], [3, 4], [5, 4], [6, 4], [7, 4],
            [0, 0], [1, 1], [2, 2], [3, 3], [5, 5], [6, 6], [7, 7],
            [1, 7], [2, 6], [3, 5], [5, 3], [6, 2], [7, 1]
        ]
        calculated_moves = self.queen.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()


if __name__ == '__main__':
    unittest.main()
