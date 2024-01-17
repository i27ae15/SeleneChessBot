import unittest

from pgn import PGN

from core.testing import print_starting, print_success


class TestPGN(unittest.TestCase):

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

    def test_pgn_string_format_castleling(self):

        pgn = "1. d4 d5 2. Bf4 e6 3. e3 Nf6 4. Nd2 Bd6 5. Bg3 c6 6. c3 O-O 7. Qc2 Re8 8. O-O-O h6"

        print_starting()
        pgn = PGN(pgn)
        print(pgn.pgn)
        print_success()


if __name__ == '__main__':
    unittest.main()
