from django.test import TestCase

from core.utils import INITIAL_FEN

from game.models import GameState
from game.game import Game


class TestGameModelSimulation(TestCase):

    def setUp(self) -> None:
        self.games_to_simulate = 10
        return super().setUp()

    def test_game_simulation(self):
        parent: GameState = GameState.objects.get(fen=INITIAL_FEN)

        for current in range(self.games_to_simulate):
            game: Game = Game.parse_fen(parent.fen)
            child_game_state, move = parent.expand(game)
            child_game_state: GameState
            r = child_game_state.simulate(
                game=Game,
                first_move=move,
                save_data=True
            )
            print(f'Game {current + 1} simulated successfully. {r}')
