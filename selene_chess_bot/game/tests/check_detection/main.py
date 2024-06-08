from unittest import TestCase

from core.testing import print_starting, print_success

from pieces.utilites import PieceName, PieceColor, RookSide

from game import Game
from game.check_detector import CheckDetector


class CheckDetectorTest(TestCase):

    def setUp(self) -> None:
        self.initialize_game()
        return super().setUp()

    def tearDown(self) -> None:
        self.initialize_game()
        return super().tearDown()

    def initialize_game(self) -> None:
        self.game = Game()
        self.game.board.clean_board()

    def load_check_detector(self):
        self.game.create_current_fen()
        self.check_detector = CheckDetector(self.game.current_fen)

    def test_two_rooks_check(self):
        """
            Situation:
            Black King on d8
            One rook on a7
            One rook on h1

            Expected:
            Rh8#
        """
        print_starting()

        # setting up pieces
        # Black King on d8
        self.game.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.BLACK,
            algebraic_notation='d8'
        )

        # Rooks
        # One rook on a7
        self.game.board.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.WHITE,
            algebraic_notation='a7',
            additional_information={
                'rook_side': RookSide.QUEEN
            }
        )

        # One rook on h1
        self.game.board.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.WHITE,
            algebraic_notation='h2',
            additional_information={
                'rook_side': RookSide.KING
            }
        )

        # white king on e1
        self.game.board.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.WHITE,
            algebraic_notation='e1'
        )

        self.game.board.print_board()
        self.load_check_detector()

        self.assertEqual(
            ['Rhh8', 'Rhd2', 'Raa8', 'Rad7'],
            self.check_detector.checks_on_position
        )

        print_success()

    def test_real_position(self):

        print_starting()

        fen = 'r1b1R3/2qn1p1k/p5p1/1p1p3p/7Q/P2B4/1bP2PPP/R5K1 w - - 1 2'

        self.game = Game.parse_fen(fen=fen)
        self.load_check_detector()

        self.assertEqual(
            ['Reh8', 'Bdxg6', 'Qhxh5'],
            self.check_detector.checks_on_position
        )

        print_success()
