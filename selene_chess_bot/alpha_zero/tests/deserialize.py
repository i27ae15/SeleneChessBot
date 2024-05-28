from django.test import TestCase

from game.game import Game

from alpha_zero.mcst import MCST
from alpha_zero.serializer import Checkpoint
from alpha_zero.tree import TreeRepresentation


class TestDeserializer(TestCase):

    def test_main(self):
        # Example usage:

        game: Game = Game()
        mcst = MCST(
            initial_fen=game.create_current_fen(),
        )
        mcst.run(10)

        best_move = max(
            mcst.root.children.values(),
            key=lambda n: n.num_visits
        )

        game = Game.parse_fen(best_move.fen)
        game.board.print_board(show_in_algebraic_notation=True)

        # checkpoint = Checkpoint()
        # root = checkpoint.load_checkpoint()
        root = mcst.root
        # print(root.fen)

        # TreeRepresentation(root)
