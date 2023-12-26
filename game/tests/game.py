import unittest

from game import Game

from pieces.utilites import PieceColor

from core.testing import print_starting, print_success


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def tearDown(self) -> None:
        self.game = Game()
        return super().tearDown()

    def test_first_moves(self):

        print_starting()

        # let's play d4 and d5

        self.game.move_piece('Pd4')

        # check if the current player is black
        self.assertEqual(
            self.game.player_turn,
            PieceColor.BLACK,
            "The current player should be black."
        )

        self.game.move_piece('Pd5')

        # check if the current player is white
        self.assertEqual(
            self.game.player_turn,
            PieceColor.WHITE,
            "The current player should be white."
        )

        # check if the current turn is 2

        self.assertEqual(
            self.game.current_turn,
            2,
            "The current turn should be 2."
        )

        print_success()

    def test_several_moves(self):

        print_starting()

        # let's play d4 and d5

        self.game.move_piece('Pd4')

        # check if the current player is black
        self.assertEqual(
            self.game.player_turn,
            PieceColor.BLACK,
            "The current player should be black."
        )

        self.game.move_piece('Pd5')

        # check if the current player is white
        self.assertEqual(
            self.game.player_turn,
            PieceColor.WHITE,
            "The current player should be white."
        )

        # check if the current turn is 2

        self.assertEqual(
            self.game.current_turn,
            2,
            "The current turn should be 2."
        )

        # let's play e4 and e5

        self.game.move_piece('Pe4')

        # check if the current player is black
        self.assertEqual(
            self.game.player_turn,
            PieceColor.BLACK,
            "The current player should be black."
        )

        self.game.move_piece('Pe5')

        # check if the current player is white
        self.assertEqual(
            self.game.player_turn,
            PieceColor.WHITE,
            "The current player should be white."
        )

        # check if the current turn is 3

        self.assertEqual(
            self.game.current_turn,
            3,
            "The current turn should be 3."
        )

        # let's play Nf3 and Nc6

        self.game.move_piece('Nf3')

        # check if the current player is black
        self.assertEqual(
            self.game.player_turn,
            PieceColor.BLACK,
            "The current player should be black."
        )

        self.game.move_piece('Nc6')

        # check if the current player is white
        self.assertEqual(
            self.game.player_turn,
            PieceColor.WHITE,
            "The current player should be white."
        )

        # check if the current turn is 4

        self.assertEqual(
            self.game.current_turn,
            4,
            "The current turn should be 4."
        )

        # let's play Nc3 and Nf6

        self.game.move_piece('Nc3')

        # check if the current player is black
        self.assertEqual(
            self.game.player_turn,
            PieceColor.BLACK,
            "The current player should be black."
        )

        self.game.move_piece('Nf6')

        print_success()

    def test_invalid_move(self):

        print_starting()

        self.game.move_piece('Pd4')
        self.game.move_piece('Pd5')

        with self.assertRaises(ValueError):
            self.game.move_piece('Pd5')

        print_success()

    def test_invalid_abbreviation(self):

        print_starting()

        self.game.move_piece('Pd4')
        self.game.move_piece('Pd5')

        with self.assertRaises(ValueError):
            self.game.move_piece('Ld5')

        print_success()

    def test_multiple_moves(self):

        print_starting()

        self.game.move_piece('Pd4')
        self.game.move_piece('Pd5')

        self.game.move_piece('Pe4')
        self.game.move_piece('Pe5')

        self.game.move_piece('Nf3')
        self.game.move_piece('Nc6')

        self.game.move_piece('Nc3')
        self.game.move_piece('Nf6')

        print(self.game.moves)
        self.game.board.print_board()

        print_success()


if __name__ == '__main__':
    unittest.main()
