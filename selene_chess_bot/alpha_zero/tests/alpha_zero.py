import unittest

from core.db import Base, config

from alpha_zero import MCTS
from game import Game


class AlphaZeroTest(unittest.TestCase):

    def setUp(self):
        self.mcts = MCTS(
            game=Game(),
            num_searches=100,
        )

    def test_mcts(self):
        try:
            print(self.mcts)
            self.mcts.search()
        except Exception as e:
            print(e)
            config.drop_test_db()
