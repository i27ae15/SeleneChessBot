from django.test import TestCase
from core.utils import INITIAL_FEN
from pgn.pgn import PGN

from core.testing import print_starting, print_success

from game.models import GameState


class TestPGN(TestCase):

    def extract_pgn_to_variables(self, file_path: str) -> list[str]:
        with open(file_path, 'r') as file:
            games = file.read().strip().split('\n\n')

        return games

    def test_string_format(self):

        print_starting()
        PGN('1.e4 e6 2.d4 d5 3.Nd2 Nf6')
        print_success()

    def test_dict_format(self):

        print_starting()
        PGN(
            {
                '1': ['e4', 'e6'],
                '2': ['d4', 'd5'],
                '3': ['Nd2', 'Nf6']
            }
        )
        print_success()

    def test_string_format_castleling(self):

        pgn = "1.d4 d5 2.Bf4 e6 3.e3 Nf6 4.Nd2 Bd6 5.Bg3 c6 6.c3 O-O 7.Qc2 Re8 8.O-O-O h6"

        print_starting()
        pgn = PGN(pgn)
        print(pgn.pgn)
        print_success()

    def test_from_real_games(self):

        print_starting()
        # Usage
        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)
        total_moves = 0

        for index, game in enumerate(pgn_games):
            g = game.replace('\n', ' ')
            print('game', index + 1)
            total_moves += PGN(g).total_moves

        print('total_moves', total_moves)
        print_success()

    def test_unique_game(self):

        print_starting()

        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)
        game = pgn_games[8].replace('\n', ' ')

        print('game', game)
        PGN(game, debug=True)
        print_success()

    def test_unique_game_stalemate(self):

        print_starting()

        # file_path = 'pgn/tests/stalemate.txt'
        file_path = 'pgn/tests/three_fold_rep.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)
        game = pgn_games[0].replace('\n', ' ')

        print('game', game)
        PGN(game, debug=True)

        print_success()

    def test_unique_game_threefold_repetition(self):
        """
        Checks for threefold repetition in a chess game.
        :param moves: A dictionary of moves made in the game.
        :return: True if threefold repetition is met, False otherwise.
        """

        print_starting()

        file_path = 'pgn/tests/three_fold_rep.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)
        game = pgn_games[0].replace('\n', ' ')

        print('game', game)
        PGN(game, debug=True)

        print_success()

    def test_multiple_parents(self):

        print_starting()

        file_path = 'pgn/tests/same_pos_diff_moves.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)


        for index, game in enumerate(pgn_games):
            g = game.replace('\n', ' ')
            print('game', index + 1)
            PGN(g)

        self.dfs(GameState.objects.get(fen=INITIAL_FEN))

        print_success()

    def dfs(self, parent: GameState):

        print('-' * 50)
        print('parents', parent.parents.all().count())
        print('-' * 50)

        if parent.children.all().count() == 0:
            return

        for child in parent.children.all():
            self.dfs(child)
