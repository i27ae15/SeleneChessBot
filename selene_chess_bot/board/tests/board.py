import unittest

from core.testing import print_starting, print_success

from board.board import Board
from board.exceptions import KingAlreadyOnBoardError

from pieces.utilites import PieceName, PieceColor


class TestBoard(unittest.TestCase):

    def test_initial_set_up(self):

        print_starting()

        board = Board()

        print('-' * 50)
        print('pieces on board')
        pieces_on_board = board.pieces_on_board[PieceColor.WHITE]
        for key in pieces_on_board:
            print(
                key.name, [
                    piece.algebraic_pos for piece in pieces_on_board[key]
                ]
            )
        print('-' * 50)

        print_success()

    def test_print_attacked_w_squares(self):

        print_starting()

        board = Board()
        board.print_attacked_squares()

        print_success()

    def test_print_attacked_squares_by_w_king(self):

        print_starting()

        board = Board()
        board.print_attacked_squares(
            piece_name=PieceName.KING,
        )
        print_success()

    def test_print_attacked_squares_by_w_queen(self):

        print_starting()

        board = Board()
        board.print_attacked_squares(
            piece_name=PieceName.QUEEN,
        )
        print_success()

    def test_print_attacked_squares_by_w_rooks(self):

        print_starting()

        board = Board()
        board.print_attacked_squares(
            piece_name=PieceName.ROOK,
        )
        print_success()

    def test_print_attacked_squares_by_w_bishops(self):

        print_starting()

        board = Board()
        board.print_attacked_squares(
            piece_name=PieceName.BISHOP,
        )
        print_success()

    def test_print_attacked_b_squares(self):

        print_starting()

        board = Board()
        board.print_attacked_squares(perspective=PieceColor.BLACK)

        print_success()

    def test_more_than_one_king_on_board(self):

        print_starting()

        board: Board = Board()
        with self.assertRaises(KingAlreadyOnBoardError):
            board.add_piece(
                piece=PieceName.KING,
                piece_color=PieceColor.WHITE,
                algebraic_notation='e1',
            )
        print_success()


if __name__ == '__main__':
    unittest.main()
