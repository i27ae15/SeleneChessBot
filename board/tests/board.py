import unittest

from core.testing import print_starting, print_success

from board import Board

from pieces.utilites import PieceName, PieceColor


class TestBoard(unittest.TestCase):

    def atest_initial_set_up(self):

        print_starting()

        board = Board()
        print(board)

        print_success()

    def test_print_attacked_w_squares(self):

        print_starting()

        board = Board()
        board.print_attacked_squares()

        print_success()

    def atest_print_attacked_squares_by_w_king(self):

        print_starting()

        board = Board()
        board.print_attacked_squares(
            piece_name=PieceName.KING,
        )
        print_success()

    def atest_print_attacked_squares_by_w_queen(self):

        print_starting()

        board = Board()
        board.print_attacked_squares(
            piece_name=PieceName.QUEEN,
        )
        print_success()

    def atest_print_attacked_squares_by_w_rooks(self):

        print_starting()

        board = Board()
        board.print_attacked_squares(
            piece_name=PieceName.ROOK,
        )
        print_success()

    def atest_print_attacked_squares_by_w_bishops(self):

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


if __name__ == '__main__':
    unittest.main()
