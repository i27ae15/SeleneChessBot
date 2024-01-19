# FILEPATH: /c:/Users/andre/Desktop/selene_chess/tests/test_piece_move.py
import unittest

from game.piece_move import PieceMove

from pieces.utilites import PieceColor, PieceName

from core.testing import print_starting, print_success


class TestPieceMove(unittest.TestCase):

    def test_moving_pawn(self):

        print_starting()

        piece_move = PieceMove('e4', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.PAWN)
        self.assertEqual(piece_move.piece_abbreviation, 'P')
        self.assertEqual(piece_move._abr_move, 'e4')
        self.assertEqual(piece_move.square, 'e4')
        self.assertEqual(piece_move.piece_file, 'e')

        print_success()

    def test_moving_knight(self):

        print_starting()

        piece_move = PieceMove('Nf3', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.KNIGHT)
        self.assertEqual(piece_move.piece_abbreviation, 'N')
        self.assertEqual(piece_move._abr_move, 'Nf3')
        self.assertEqual(piece_move.square, 'f3')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_bishop(self):

        print_starting()

        piece_move = PieceMove('Bc4', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.BISHOP)
        self.assertEqual(piece_move.piece_abbreviation, 'B')
        self.assertEqual(piece_move._abr_move, 'Bc4')
        self.assertEqual(piece_move.square, 'c4')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_rook(self):

        print_starting()

        piece_move = PieceMove('Ra1', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.ROOK)
        self.assertEqual(piece_move.piece_abbreviation, 'R')
        self.assertEqual(piece_move._abr_move, 'Ra1')
        self.assertEqual(piece_move.square, 'a1')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_queen(self):

        print_starting()

        piece_move = PieceMove('Qd2', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.QUEEN)
        self.assertEqual(piece_move.piece_abbreviation, 'Q')
        self.assertEqual(piece_move._abr_move, 'Qd2')
        self.assertEqual(piece_move.square, 'd2')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_king(self):

        print_starting()

        piece_move = PieceMove('Ke2', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'Ke2')
        self.assertEqual(piece_move.square, 'e2')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_knight_capture(self):

        print_starting()

        piece_move = PieceMove('Nxe4', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.KNIGHT)
        self.assertEqual(piece_move.piece_abbreviation, 'N')
        self.assertEqual(piece_move._abr_move, 'Ne4')
        self.assertEqual(piece_move.square, 'e4')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_moving_knight_in_the_same_file(self):

        print_starting()

        piece_move = PieceMove('Ngf3', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.KNIGHT)
        self.assertEqual(piece_move.piece_abbreviation, 'N')
        self.assertEqual(piece_move._abr_move, 'Ngf3')
        self.assertEqual(piece_move.square, 'f3')
        self.assertEqual(piece_move.piece_file, 'g')

        print_success()

    def test_invalid_move(self):

        print_starting()

        with self.assertRaises(ValueError):
            PieceMove('jkn', PieceColor.WHITE)

        print_success()

    def test_white_castleling_short(self):

        print_starting()

        piece_move = PieceMove('O-O', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'O-O')
        self.assertEqual(piece_move.square, 'g1')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_white_castleling_long(self):

        print_starting()

        piece_move = PieceMove('O-O-O', PieceColor.WHITE)

        self.assertEqual(piece_move.piece, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'O-O-O')
        self.assertEqual(piece_move.square, 'c1')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_black_castleling_short(self):

        print_starting()

        piece_move = PieceMove('O-O', PieceColor.BLACK)

        self.assertEqual(piece_move.piece, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'O-O')
        self.assertEqual(piece_move.square, 'g8')
        self.assertEqual(piece_move.piece_file, None)

        print_success()

    def test_black_castleling_long(self):

        print_starting()

        piece_move = PieceMove('O-O-O', PieceColor.BLACK)

        self.assertEqual(piece_move.piece, PieceName.KING)
        self.assertEqual(piece_move.piece_abbreviation, 'K')
        self.assertEqual(piece_move._abr_move, 'O-O-O')
        self.assertEqual(piece_move.square, 'c8')
        self.assertEqual(piece_move.piece_file, None)

        print_success()


if __name__ == '__main__':
    unittest.main()
