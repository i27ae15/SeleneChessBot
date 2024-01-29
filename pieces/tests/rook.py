import unittest

from core.testing import print_starting, print_success

from board import Board

from pieces import Rook

from pieces.utilites import PieceColor, PieceName


class TestRook(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board.create_empty_board()
        self.rook = self.add_rook_to_board()

    def tearDown(self) -> None:
        self.board.clean_board()
        self.rook = self.add_rook_to_board()

    def add_rook_to_board(self, row: int = 4, column: int = 4) -> Rook:
        return self.board.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.WHITE,
            row=row,
            column=column
        )

    def test_calculate_legal_moves(self):
        print_starting()
        expected_moves = [
            [4, 0], [4, 1], [4, 2], [4, 3], [4, 5], [4, 6], [4, 7],
            [0, 4], [1, 4], [2, 4], [3, 4], [5, 4], [6, 4], [7, 4]
        ]
        calculated_moves = self.rook.calculate_legal_moves()
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
            'd5', 'f5', 'g5', 'h5'
        ]
        self.assertEqual(
            sorted(
                self.rook.calculate_legal_moves(
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
            row=0,
            column=4
        )

        expected_moves = [
            [4, 0], [4, 1], [4, 2], [4, 3], [4, 5], [4, 6], [4, 7],
            [0, 4], [1, 4], [2, 4], [3, 4], [5, 4], [6, 4], [7, 4]
        ]
        calculated_moves = self.rook.calculate_legal_moves()
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
            row=0,
            column=4
        )
        expected_moves = [
            [4, 0], [4, 1], [4, 2], [4, 3], [4, 5], [4, 6], [4, 7],
            [1, 4], [2, 4], [3, 4], [5, 4], [6, 4], [7, 4]
        ]
        calculated_moves = self.rook.calculate_legal_moves()
        calculated_moves = [list(move) for move in calculated_moves]

        self.assertEqual(
            sorted(calculated_moves),
            sorted(expected_moves)
        )

        print_success()

    def test_scan_row_when_piece_in_corner(self):

        print_starting()

        rook: Rook = self.add_rook_to_board(row=0, column=0)
        expected_moves_algebraic = [
            'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'c1', 'd1',
            'e1', 'f1', 'g1', 'h1'
        ]
        rook.scan_row()
        rook.scan_column()

        legal_moves = rook.calculate_legal_moves(
            show_in_algebraic_notation=True
        )

        self.assertEqual(
            sorted(legal_moves),
            sorted(expected_moves_algebraic)
        )

        print_success()

    def test_legal_moves_with_king_next_to_piece_in_diagonal(self):

        print_starting()
        self.board.clean_board()

        q = self.board.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.WHITE,
            row=4,
            column=4
        )

        self.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.WHITE,
            row=5,
            column=5
        )

        # also, add a eneymy bishop in the same diagonal
        self.board.add_piece(
            piece=PieceName.BISHOP,
            piece_color=PieceColor.BLACK,
            row=0,
            column=0
        )

        self.board.print_board()
        legal_moves = q.calculate_legal_moves(
            show_in_algebraic_notation=True
        )
        print('legal_moves', legal_moves)
        print_success()


if __name__ == '__main__':
    unittest.main()
