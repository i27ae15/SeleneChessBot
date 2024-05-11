import unittest

from core.testing import print_starting, print_success

from game.piece_move import PieceMove
from game.exceptions import InvalidMoveError

from pieces.utilites import PieceColor, PieceName

from board.board import Board


class TestPieceMove(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board()
        return super().setUp()

    def tearDown(self) -> None:
        self.board = Board()
        return super().tearDown()

    def test_moving_pawn(self):

        print_starting()

        piece_move = PieceMove(
            move='e4',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.PAWN)
        self.assertEqual(piece_move.piece_abbreviation, 'P')
        self.assertEqual(piece_move._abr_move, 'e4')
        self.assertEqual(piece_move.square, 'e4')
        self.assertEqual(piece_move.piece_file, 'e')

        print_success()

    def test_moving_knight(self):

        print_starting()

        piece_move = PieceMove(
            move='Nf3',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.KNIGHT)
        self.assertEqual(piece_move.piece_abbreviation, 'N')
        self.assertEqual(piece_move._abr_move, 'Nf3')
        self.assertEqual(piece_move.square, 'f3')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_bishop(self):

        print_starting()

        piece_move = PieceMove(
            move='Bc4',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.BISHOP)
        self.assertEqual(piece_move.piece_abbreviation, 'B')
        self.assertEqual(piece_move._abr_move, 'Bc4')
        self.assertEqual(piece_move.square, 'c4')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_rook(self):

        print_starting()

        piece_move = PieceMove(
            move='Ra1',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.ROOK)
        self.assertEqual(piece_move.piece_abbreviation, 'R')
        self.assertEqual(piece_move._abr_move, 'Ra1')
        self.assertEqual(piece_move.square, 'a1')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_queen(self):

        print_starting()

        piece_move = PieceMove(
            move='Qd2',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.QUEEN)
        self.assertEqual(piece_move.piece_abbreviation, 'Q')
        self.assertEqual(piece_move._abr_move, 'Qd2')
        self.assertEqual(piece_move.square, 'd2')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_king(self):

        print_starting()

        piece_move = PieceMove(
            move='Ke2',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'Ke2')
        self.assertEqual(piece_move.square, 'e2')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_knight_capture(self):

        print_starting()

        piece_move = PieceMove(
            move='Nxe4',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.KNIGHT)
        self.assertEqual(piece_move.piece_abbreviation, 'N')
        self.assertEqual(piece_move._abr_move, 'Ne4')
        self.assertEqual(piece_move.square, 'e4')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_knight_in_the_same_file(self):

        print_starting()

        piece_move = PieceMove(
            move='Ngf3',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.KNIGHT)
        self.assertEqual(piece_move.piece_abbreviation, 'N')
        self.assertEqual(piece_move._abr_move, 'Ngf3')
        self.assertEqual(piece_move.square, 'f3')
        self.assertEqual(piece_move.piece_file, 'g')

        print_success()

    def test_invalid_move(self):

        print_starting()

        with self.assertRaises(InvalidMoveError):
            PieceMove(
                move='jkn',
                player_turn=PieceColor.WHITE,
                board=self.board
            )

        print_success()

    def test_white_castleling_short(self):

        print_starting()

        piece_move = PieceMove(
            move='O-O',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'O-O')
        self.assertEqual(piece_move.square, 'g1')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_white_castleling_long(self):

        print_starting()

        piece_move = PieceMove(
            move='O-O-O',
            player_turn=PieceColor.WHITE,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'O-O-O')
        self.assertEqual(piece_move.square, 'c1')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_black_castleling_short(self):

        print_starting()

        piece_move = PieceMove(
            move='O-O',
            player_turn=PieceColor.BLACK,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'O-O')
        self.assertEqual(piece_move.square, 'g8')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_black_castleling_long(self):

        print_starting()

        piece_move = PieceMove(
            move='O-O-O',
            player_turn=PieceColor.BLACK,
            board=self.board
        )

        self.assertEqual(piece_move.piece_name, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'O-O-O')
        self.assertEqual(piece_move.square, 'c8')
        self.assertEqual(piece_move.piece_file, None)

        print_success()


if __name__ == '__main__':
    unittest.main()
