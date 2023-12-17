# FILEPATH: /c:/Users/andre/Desktop/selene_chess/pieces/tests/king.py
import unittest

from core.testing import print_starting, print_success

from board import Board
from core.utils import convert_to_algebraic_notation

from pieces import King

from pieces.utilites import PieceColor, PieceName


class TestKing(unittest.TestCase):

    def setUp(self):
        self.board = Board(create_initial_board_set_up=False)
        self.board.create_empty_board()
        self.king = self.add_king_to_board()
        self.board.no_castleling_rights(color=PieceColor.WHITE)

    def tearDown(self) -> None:
        self.board.clean_board()

        self.king = self.add_king_to_board()
        return super().tearDown()

    def add_king_to_board(self, row: int = 4, column: int = 4) -> King:
        return self.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.WHITE,
            row=row,
            column=column
        )

    def test_calculate_legal_moves(self):
        print_starting()
        expected_moves = [
            [3, 3], [3, 4], [3, 5], [4, 3], [4, 5], [5, 3], [5, 4], [5, 5]
        ]
        calculated_moves = self.king.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()

    def test_calculate_legal_moves_with_algebraic_notation(self):
        print_starting()
        expected_moves = [
            'd4', 'd5', 'd6', 'e4', 'e6', 'f4', 'f5', 'f6'
        ]
        self.assertEqual(
            sorted(
                self.king.calculate_legal_moves(
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
            column=5
        )
        expected_moves = [
            [3, 3], [3, 4], [3, 5], [4, 3], [4, 5], [5, 3], [5, 4], [5, 5]
        ]
        calculated_moves = self.king.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()

    def test_enemy_queen_on_legal_move(self):
        print_starting()
        q = self.board.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.BLACK,
            row=5,
            column=5
        )
        expected_moves = [
            'd5', 'e4', 'f6'
        ]
        calculated_moves = self.king.calculate_legal_moves(
            show_in_algebraic_notation=True
        )

        attacked_squares = self.board.get_attacked_squares(
            color=PieceColor.BLACK,
            show_in_algebraic_notation=True
        )
        algebraic_list = list()

        for move in attacked_squares:
            algebraic_list.append(convert_to_algebraic_notation(*move))

        print('att', q.calculate_legal_moves(show_in_algebraic_notation=True))

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()

    def test_friendly_piece_on_legal_move(self):
        print_starting()
        self.board.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.WHITE,
            row=5,
            column=5
        )

        expected_moves = [
            [3, 3], [3, 4], [3, 5], [4, 3], [4, 5], [5, 3], [5, 4]
        ]
        calculated_moves = self.king.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()


if __name__ == '__main__':
    unittest.main()
