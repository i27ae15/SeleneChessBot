from django.test import TestCase

from game.models import GameState
from game.game import Game


class TestGameModel(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        return super().setUp()

    def test_move_creation(self):

        self.game.move_piece('Pe4')
        self.game.move_piece('Pe5')

        self.game.move_piece('Qh5')
        self.game.move_piece('Pa6')

        self.game.move_piece('Qe5')

        total_objects = GameState.objects.all().count()
        # create a new game

        self.game = Game()

        self.game.move_piece('Pe4')
        self.game.move_piece('Pe5')

        self.game.move_piece('Qh5')
        self.game.move_piece('Pa6')

        self.game.move_piece('Qe5')

        self.assertEqual(GameState.objects.all().count(), total_objects)

        print(GameState.objects.all().last().num_visits)




