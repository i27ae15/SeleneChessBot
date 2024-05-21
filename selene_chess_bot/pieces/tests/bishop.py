import unittest

from core.testing import print_starting, print_success

from board import Board

from pieces import Bishop

from pieces.utilites import PieceColor, PieceName


class TestBishop(unittest.TestCase):

    def setUp(self):
        self.board = Board(board_setup='empty')
        self.bishop = self.add_bishop_to_board()

    def tearDown(self) -> None:
        self.board.clean_board()
        self.bishop = self.add_bishop_to_board()
        return super().tearDown()

    def add_bishop_to_board(self, row: int = 4, column: int = 4) -> Bishop:
        return self.board.add_piece(
            piece=PieceName.QUEEN,
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

    def test_move_when_friendly_k_is_being_proteced_on_d(self):

        print_starting()

        self.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.WHITE,
            row=5,
            column=5
        )

        # put a Queen on the board
        self.board.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.BLACK,
            row=0,
            column=0
        )
        # On diagonals it is working
        m = self.bishop.calculate_legal_moves(show_in_algebraic_notation=True)
        possible_moves = ['d4', 'c3', 'b2', 'a1']

        self.assertEqual(
            sorted(m),
            sorted(possible_moves)
        )

        print_success()

    def test_move_when_friendly_k_is_being_proteced_on_row(self):

        print_starting()

        self.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.WHITE,
            row=4,
            column=5
        )

        # put a Rook on the board
        self.board.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.BLACK,
            row=4,
            column=0
        )

        # put a Queen on f1
        self.board.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.BLACK,
            row=0,
            column=5
        )

        self.board.print_board(show_in_algebraic_notation=True)
        m = self.bishop.calculate_legal_moves(show_in_algebraic_notation=True)

        print(m)
        print_success()


if __name__ == '__main__':
    unittest.main()
