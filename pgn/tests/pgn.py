import unittest

from pgn import PGN

from core.testing import print_starting, print_success
from pieces.utilites import PieceColor, PieceName


class TestPGN(unittest.TestCase):

    def extract_pgn_to_variables(self, file_path: str) -> list[str]:
        with open(file_path, 'r') as file:
            games = file.read().strip().split('\n\n')

        return games

        pgn_variables = {}
        for i, game in enumerate(games):
            var_name = f"var{i+1}"
            pgn_variables[var_name] = game.replace('\n', ' ')

        return pgn_variables

    def atest_pgn_string_format(self):

        print_starting()
        pgn = PGN('1. e4 e6 2. d4 d5 3. Nd2 Nf6')
        print_success()

    def atest_pgn_dict_format(self):

        print_starting()
        pgn = PGN(
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

    def test_pgn_from_real_game(self):

        print_starting()
        # Usage
        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)

        for game in pgn_games:
            g = game.replace('\n', ' ')
            print(g)
            pgn = PGN(g)
            break
        print_success()


if __name__ == '__main__':
    unittest.main()
