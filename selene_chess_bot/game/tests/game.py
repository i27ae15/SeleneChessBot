from django.test import TestCase

from core.testing import print_starting, print_success

from pieces.utilites import PieceColor

from game.game import Game
from game.exceptions import InvalidMoveError


class TestGame(TestCase):

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

        with self.assertRaises(InvalidMoveError):
            self.game.move_piece('Pd5')

        print_success()

    def test_invalid_abbreviation(self):

        print_starting()

        self.game.move_piece('Pd4')
        self.game.move_piece('Pd5')

        with self.assertRaises(InvalidMoveError):
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

        print_success()

    def test_en_passant_tracking(self):

        print_starting()

        self.game.move_piece('Pa4')
        self.game.move_piece('Pd5')

        self.game.move_piece('Pa5')
        self.game.move_piece('Pd4')

        self.game.move_piece('Pe4')

        print_success()

    def test_capture_en_passant(self):

        print_starting()

        self.game.move_piece('Pa4')
        self.game.move_piece('Pd5')

        self.game.move_piece('Pa5')
        self.game.move_piece('Pd4')

        self.game.move_piece('Pe4')

        # get the pawn on d4
        pawn = self.game.board.get_square_or_piece(row=3, column=3)
        legal_moves = pawn.calculate_legal_moves(True)

        # check if the pawn can capture en passant

        self.assertIn('e3', legal_moves)
        self.game.move_piece('Pdxe3')

        self.game.board.print_board()

        print_success()

    def test_moving_into_check(self):

        print_starting()

        self.game.move_piece('Pe4')
        self.game.move_piece('Pe5')

        self.game.move_piece('Qh5')
        self.game.move_piece('Nc6')

        self.game.move_piece('Qf7')

        with self.assertRaises(InvalidMoveError):
            self.game.move_piece('Pa5')

        print_success()

    def test_check_state(self):

        print_starting()

        self.game.move_piece('Pe4')
        self.game.move_piece('Pe5')

        self.game.move_piece('Qh5')
        self.game.move_piece('Pa6')

        self.game.move_piece('Qe5')

        self.game.print_game_state()
        self.game.board.print_board()

        print_success()

    def test_generate_fen(self):

        print_starting()
        print(self.game.create_current_fen())
        print_success()

    def test_parse_fen(self):

        print_starting()

        fen_list = [
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "r1bq1rk1/ppp1bppp/2n2n2/3pp3/3P4/2PB1N2/PP3PPP/RNBQ1RK1 w - c6 0 10",
            "6k1/5ppp/8/8/2B5/2P5/PP3PPP/6K1 b - - 0 30",
            "rnb1kbnr/pppp1ppp/8/4p3/2B1P3/8/PPP2PPP/RNBQK1NR b KQkq - 0 3",
            "rnbq1rk1/ppp2ppp/5n2/3pp3/3P4/5NP1/PPP1PPBP/RNBQ1RK1 w Kk - 4 6"
        ]

        for fen in fen_list:
            game: Game = self.game.parse_fen(fen)
            print('-' * 50)
            game.board.print_board()
            print('-' * 50)

        print_success()


class TestSelfChessGame(TestCase):

    def setUp(self) -> None:
        self.game: Game = Game()
        return super().setUp()

    def test_start(self):
        self.game.start()
