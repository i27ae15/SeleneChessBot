from django.test import TestCase
from alpha_zero.alpha_zero import AlphaZero


class AlphaZeroTest(TestCase):

    def test_alpha_zero(self):

        alpha_zero = AlphaZero(
            depth_of_search=10,
        )
        game = alpha_zero.play_game()
        game.print_game_state()
