import unittest

from alpha_zero.mcts import MCTS
from game.game import Game


class AlphaZeroTest(unittest.TestCase):

    def setUp(self):
        self.mcts = MCTS(
            game=Game(),
            num_searches=100,
        )

    def test_mcts(self):
        pass
