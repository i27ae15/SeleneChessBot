
from django.core.management.base import BaseCommand

from core.utils import INITIAL_FEN

from game.models import GameState
from game.game import Game


class Command(BaseCommand):
    help = 'Test the creation of GameState objects from the create_obj_from_pgn.py file.'

    def handle(self, *args, **options):

        self.view_game()

    def view_game(self):

        save_games: list[GameState] = []
        parent = GameState.objects.get(fen=INITIAL_FEN)
        self.dfs_on_visits(
            parent=parent,
            save_games=save_games
        )

        for i, game in enumerate(save_games):
            print('-' * 50)
            print('move:', (i + 1) // 2)
            print('fen:', game.fen)
            g = Game.parse_fen(game.fen)
            g.board.print_board()
            print('-' * 50)
        print('Number of game states:', len(save_games))

    def test_first_game_state(self):

        # check that the initial game has visited 198 times
        # get the first initial_game_state

        initial_game_state = GameState.objects.get(fen=INITIAL_FEN)
        print('-' * 50)
        print('Initial Game State:', initial_game_state.num_visits)
        print('children should be 6', initial_game_state.children.all().count() == 6)
        print('-' * 50)

    def print_children(self, parent: GameState):

        for child in parent.children.all():
            child: GameState
            print('-' * 50)
            print(child.fen, child.num_visits)

            g = Game.parse_fen(child.fen)
            g.print_game_state()

            g.board.print_board()

            print('-' * 50)

    def dfs_on_visits(
        self,
        parent: GameState,
        save_games: list[GameState] = None
    ):

        if save_games is not None:
            save_games.append(parent)

        if parent.children.all().count() == 0:
            return

        # go for the children with the most visits

        children = parent.children.all().order_by('-num_visits')
        child = children.first()
        self.dfs_on_visits(child, save_games)
