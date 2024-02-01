import unittest

from pgn import PGN

from core.testing import print_starting, print_success
from pieces.king import King
from pieces.utilites import PieceColor, PieceName


class TestPGN(unittest.TestCase):

    def extract_pgn_to_variables(self, file_path: str) -> list[str]:
        with open(file_path, 'r') as file:
            games = file.read().strip().split('\n\n')

        return games

    def atest_pgn_string_format(self):

        print_starting()
        PGN('1. e4 e6 2. d4 d5 3. Nd2 Nf6')
        print_success()

    def atest_pgn_dict_format(self):

        print_starting()
        PGN(
            {
                '1': ['e4', 'e6'],
                '2': ['d4', 'd5'],
                '3': ['Nd2', 'Nf6']
            }
        )
        print_success()

    def atest_pgn_string_format_castleling(self):

        pgn = "1. d4 d5 2. Bf4 e6 3. e3 Nf6 4. Nd2 Bd6 5. Bg3 c6 6. c3 O-O 7. Qc2 Re8 8. O-O-O h6"

        print_starting()
        pgn = PGN(pgn)
        print(pgn.pgn)
        print_success()

    def atest_pgn_from_real_game(self):

        print_starting()
        # Usage
        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)

        for index, game in enumerate(pgn_games):
            g = game.replace('\n', ' ')
            print('game', index + 1)
            PGN(g)
        print_success()

    def atest_unique_game(self):

        print_starting()

        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)
        game = pgn_games[18].replace('\n', ' ')

        print('game', game)
        PGN(game, debug=True)
        print_success()

    def test_unique_game_stalemate(self):

        print_starting()

        file_path = 'pgn/tests/stalemate.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)
        game = pgn_games[0].replace('\n', ' ')

        print('game', game)
        PGN(game, debug=True)

        print_success()


if __name__ == '__main__':
    unittest.main()
