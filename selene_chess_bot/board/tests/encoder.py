from unittest import TestCase

from core.testing import print_starting, print_success

from board import Board
from board.encoder import BoardEncoder


class TestBoardEncoder(TestCase):

    def test_encode_initial_board(self):
        print_starting()

        board = Board()
        encoded_board = BoardEncoder.encode_board(board)
        BoardEncoder.visualize_encoded_board(encoded_board)

        print_success()
