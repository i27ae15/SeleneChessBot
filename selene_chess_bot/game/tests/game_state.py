from django.test import TestCase

from core.utils import INITIAL_FEN

from game.models import GameState
from game.game import Game


class TestGameModel(TestCase):

    def test_move_creation(self):
        game = Game()

        game.move_piece('Pe4')
        game.move_piece('Pe5')

        game.move_piece('Qh5')
        game.move_piece('Pa6')

        game.move_piece('Qe5')

        total_objects = GameState.objects.all().count()
        # create a new game

        game = Game()

        game.move_piece('Pe4')
        game.move_piece('Pe5')

        game.move_piece('Qh5')
        game.move_piece('Pa6')

        game.move_piece('Qe5')

        self.assertEqual(GameState.objects.all().count(), total_objects)

    def test_children_and_parent(self):

        moves_for_white: str = [
            'Pa3', 'Pa4', 'Pb3', 'Pb4', 'Pc3', 'Pc4', 'Pd3', 'Pd4', 'Pe3',
            'Pe4', 'Pf3', 'Pf4', 'Pg3', 'Pg4', 'Ph3', 'Ph4',
        ]

        moves_for_black: str = [
            'Pa6', 'Pa5', 'Pb6', 'Pb5', 'Pc6', 'Pc5', 'Pd6', 'Pd5', 'Pe6',
            'Pe5', 'Pf6', 'Pf5', 'Pg6', 'Pg5', 'Ph6', 'Ph5',
        ]

        for i in range(0, len(moves_for_white)):
            game = Game()
            game.move_piece(moves_for_white[i])
            game.move_piece(moves_for_black[i])

        # the initial position should have a total of 16 children

        initial_position: GameState = GameState.objects.get(fen=INITIAL_FEN)
        # counts its children

        self.assertEqual(initial_position.children.count(), 16)








