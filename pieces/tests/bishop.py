import unittest

from core.testing import print_starting, print_success

from board import Board

from pieces import Bishop

from pieces.utilites import PieceColor, PieceName


class TestBishop(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board.create_empty_board()
        self.bishop = self.add_bishop_to_board()

    def tearDown(self) -> None:
        self.board.clean_board()
        self.bishop = self.add_bishop_to_board()
        return super().tearDown()

    def add_bishop_to_board(self, row: int = 4, column: int = 4) -> Bishop:
        return self.board.add_piece(
            piece=PieceName.BISHOP,
            piece_color=PieceColor.WHITE,
            row=row,
            column=column
        )

    def test_calculate_legal_moves(self):
        print_starting()

        expected_moves = [
            (3, 3), (2, 2), (1, 1), (0, 0), (3, 5), (2, 6), (1, 7), (5, 3),
            (6, 2), (7, 1), (5, 5), (6, 6), (7, 7)
        ]

        self.assertEqual(
            self.bishop.calculate_legal_moves(),
            expected_moves
        )
        print_success()

    def test_calculate_legal_moves_with_algebraic_notation(self):
        print_starting()

        expected_moves = [
            'a1', 'b2', 'b8', 'c3', 'c7', 'd4', 'd6', 'f4', 'f6', 'g3', 'g7',
            'h2', 'h8'
        ]

        self.assertEqual(
            sorted(
                self.bishop.calculate_legal_moves(
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
            (3, 3), (2, 2), (1, 1), (0, 0), (3, 5), (2, 6), (1, 7), (5, 3),
            (6, 2), (7, 1), (5, 5), (6, 6), (7, 7)
        ]
        self.assertEqual(
            self.bishop.calculate_legal_moves(),
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
            (3, 3), (2, 2), (1, 1), (0, 0), (3, 5), (2, 6), (1, 7), (5, 3),
            (6, 2), (7, 1), (5, 5), (6, 6), (7, 7)
        ]

        self.assertEqual(
            self.bishop.calculate_legal_moves(),
            expected_moves
        )

        print_success()


if __name__ == '__main__':
    unittest.main()
