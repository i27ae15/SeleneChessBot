import unittest

from core.testing import print_starting, print_success

from board import Board

from pieces import Pawn
from pieces.utilites import PieceColor, PieceName


class TestPawn(unittest.TestCase):

    def setUp(self):
        self.board = Board(create_initial_board_set_up=False)
        self.board.create_empty_board()
        self.pawn = self.add_pawn_to_board()
        self.board.remove_castleling_rights(color=PieceColor.WHITE)

    def tearDown(self) -> None:
        self.board.clean_board()
        self.pawn = self.add_pawn_to_board()
        return super().tearDown()

    def add_pawn_to_board(self, row: int = 4, column: int = 4) -> Pawn:
        pawn = self.board.add_piece(
            piece=PieceName.PAWN,
            piece_color=PieceColor.WHITE,
            row=row,
            column=column
        )

        pawn.first_move = False
        return pawn

    def test_calculate_legal_moves(self):
        print_starting()
        # Adjust expected_moves according to the Pawn's movement rules
        expected_moves = [
            [5, 4]
        ]
        calculated_moves = self.pawn.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()

    def test_calculate_legal_moves_with_algebraic_notation(self):
        print_starting()
        # Adjust expected_moves according to the Pawn's movement rules
        expected_moves = [
            'e6'
        ]
        self.assertEqual(
            sorted(
                self.pawn.calculate_legal_moves(
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
            column=4
        )
        # Adjust expected_moves according to the Pawn's movement rules
        calculated_moves = self.pawn.calculate_legal_moves()

        self.assertFalse(calculated_moves)
        print_success()

    def test_friendly_piece_on_legal_move(self):
        print_starting()
        self.board.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.WHITE,
            row=5,
            column=4
        )

        # Adjust expected_moves according to the Pawn's movement rules
        calculated_moves = self.pawn.calculate_legal_moves()
        self.assertFalse(calculated_moves)

        print_success()

    def test_get_attacked_squares(self):
        print_starting()
        expected_moves = [
            [5, 3], [5, 5]
        ]
        calculated_moves = self.pawn.get_attacked_squares()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()

    def check_is_enemy_piece_can_be_taken(self):
        print_starting()
        self.board.add_piece(
            piece=PieceName.PAWN,
            piece_color=PieceColor.BLACK,
            row=5,
            column=5
        )
        expected_moves = [
            [5, 5], [5, 4]
        ]
        calculated_moves = self.pawn.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()

    def test_check_double_move_in_beginning(self):
        print_starting()
        self.pawn.first_move = True
        expected_moves = [
            [5, 4], [6, 4]
        ]
        calculated_moves = self.pawn.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )
        print_success()


if __name__ == '__main__':
    unittest.main()
