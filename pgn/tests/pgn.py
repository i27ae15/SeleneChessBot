import unittest

from pgn import PGN

from core.testing import print_starting, print_success
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

    def qtest_pgn_from_real_game(self):

        print_starting()
        # Usage
        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)

        for index, game in enumerate(pgn_games):
            g = game.replace('\n', ' ')
            print('game', index + 1)
            PGN(g)
            if index == 5:
                break
        print_success()

    def test_unique_game(self):

        print_starting()
        game = "1.e4 e5 2.f4 exf4 3.Nf3 g5 4.h4 g4 5.Ne5 Bg7 6.Nxg4 d5 7.exd5 Qe7+ 8.Kf2 Bd4+ 9.Kf3 h5 10.Bb5+ Kd8 11.Nf2 Bg4+ 12.Nxg4 hxg4+ 13.Kxg4 Nf6+ 14.Kh3 Rxh4+ 15.Kxh4 Ne4+ 16.Kg4 Nf2+ 17.Kh5 Qe5+ 18.Kh4 Qf6+ 19.Kh5 Qg6+ 20.Kh4 Bf6+"

        p = PGN(game)

        p.game.board.print_attacked_squares(
            perspective=PieceColor.BLACK,
            traspass_king=True,
            show_in_algebraic_notation=True,
        )

        # print('-' * 50)
        # print('pieces on board')
        # pieces_on_board = p.game.board.pieces_on_board[PieceColor.BLACK]
        # for key in pieces_on_board:
        #     print(key.name, [piece.algebraic_pos for piece in pieces_on_board[key]])
        # print('-' * 50)

        # for piece in PieceName.__members__.values():
        #     print('-' * 50)
        #     print('piece_name', piece.name)
        #     p.game.board.print_attacked_squares(
        #         perspective=PieceColor.BLACK,
        #         traspass_king=True,
        #         show_in_algebraic_notation=True,
        #         piece_name=piece
        #     )
        #     print('-' * 50)


if __name__ == '__main__':
    unittest.main()
