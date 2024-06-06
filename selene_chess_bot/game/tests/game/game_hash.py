from django.test import TestCase

from core.testing import print_starting, print_success

from game.game import Game


class TestGameHash(TestCase):

    def test_game_hash(self):

        print_starting()
        game = Game()

        # get the next state of the game

        next_states = game.get_next_states()

        for key, value in next_states.items():
            print(key, value)

        print_success()
