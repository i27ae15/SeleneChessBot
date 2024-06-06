from django.test import TestCase

from game.game import Game
from pieces.utilites import PieceName, PieceColor, RookSide

from alpha_zero.mcst import MCST


class TestCheckmateWhite(TestCase):

    def setUp(self) -> None:
        self.game: Game = Game()
        self.game.board.clean_board()
        return super().setUp()

    def test_checkmate_two_rooks(self):
        """
            Situation:
            Black King on d8
            One rook on a7
            One rook on h1

            Expected:
            Rh8#
        """

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
            algebraic_notation='h1',
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

        self.game.board.remove_castleling_rights(PieceColor.WHITE)
        self.game.board.remove_castleling_rights(PieceColor.BLACK)

        self.game.create_current_fen()

        mcst = MCST(initial_fen=self.game.current_fen)
        best_move = mcst.run(iterations=200)
        self.game.move_piece(best_move)
        self.game.board.print_board(show_in_algebraic_notation=True)
        print(best_move)
