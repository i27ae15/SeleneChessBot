from unittest import TestCase

from core.testing import print_starting, print_success

from game.game import Game
from pieces.utilites import PieceName, PieceColor, RookSide

from alpha_zero.mcst import MCST


class TestCheckmateBlack(TestCase):

    def setUp(self) -> None:
        self.initialize_game()
        return super().setUp()

    def tearDown(self) -> None:
        self.initialize_game()
        return super().tearDown()

    def initialize_game(self) -> None:
        self.game = Game()
        self.game.board.clean_board()

    def load_mcst(self):
        self.game.player_turn = PieceColor.BLACK
        self.game.create_current_fen()
        self.mcst = MCST(initial_fen=self.game.current_fen)

    def run_all_tests(self):
        """
            Run all the tests
        """
        methods = [
            getattr(self, method) for method in dir(self)
            if callable(getattr(self, method)) and method.startswith('t_')
        ]

        for method in methods:
            self.initialize_game()
            method()

    def t_checkmate_two_rooks(self):
        """
            Situation:
            White King on d8
            One rook on a7
            One rook on h1

            Expected:
            Rh8#
        """
        print_starting()

        # setting up pieces
        # White King on d8
        self.game.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.WHITE,
            algebraic_notation='d8'
        )

        # Rooks
        # One rook on a7
        self.game.board.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.BLACK,
            algebraic_notation='a7',
            additional_information={
                'rook_side': RookSide.QUEEN
            }
        )

        # One rook on h1
        self.game.board.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.BLACK,
            algebraic_notation='h2',
            additional_information={
                'rook_side': RookSide.KING
            }
        )

        # BLACK king on e1
        self.game.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.BLACK,
            algebraic_notation='e1'
        )

        self.load_mcst()
        best_move = self.mcst.run(iterations=200)
        self.game.move_piece(best_move)
        self.game.board.print_board(show_in_algebraic_notation=True)
        self.assertEqual(best_move, 'Rhh8')

        print_success()

    def t_checkmate_king_and_queen(self):
        """
            Situation:
            Black King on d8

            Whie King on d7
            One queen on h1

            Expected:
            Qh8#
        """

        print_starting()
        # add the white king
        self.game.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.WHITE,
            algebraic_notation='d8'
        )

        # add the black king
        self.game.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.BLACK,
            algebraic_notation='d6'
        )

        # add the black queen
        self.game.board.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.BLACK,
            algebraic_notation='h1'
        )

        self.game.board.print_board()

        self.load_mcst()
        best_move = self.mcst.run(iterations=200)
        self.game.move_piece(best_move)
        best_moves = ['Qh8', 'Qa8']
        self.assertIn(best_move, best_moves)
        print_success()

    def t_checkmate_in_two(self):
        """
            Situation:
            Black King on h1

            White King in f3
            One Queen on a8

            Expected:
        """

        print_starting()

        # add the black king
        self.game.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.BLACK,
            algebraic_notation='h1'
        )

        # add the white king
        self.game.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.WHITE,
            algebraic_notation='f3'
        )

        # add the white queen
        self.game.board.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.WHITE,
            algebraic_notation='a8'
        )

        self.load_mcst()
        best_move = self.mcst.run(iterations=1000)
        self.game.move_piece(best_move)
        # Best moves are Kf2 or Kg3
        self.game.board.print_board(show_in_algebraic_notation=True)
        print_success()

    def t_real_position_mate_in_two(self):

        fen = 'r1b1R3/2qn1p1k/p5p1/1p1p3p/7Q/P2B4/1bP2PPP/R5K1 w - - 1 2'
        mcst = MCST(initial_fen=fen)
        mcst.run(iterations=5000)

    def test_run_tests(self):
        """
            Since running all the test could take a significant amount of time,
            this method is used to run a single test if needed.

            If you want to run all the tests, use the `run_all_tests` method.
        """
        self.t_checkmate_king_and_queen()
