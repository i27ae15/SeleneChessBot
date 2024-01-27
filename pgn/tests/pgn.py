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

    def test_pgn_from_real_game(self):

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
        game = pgn_games[192].replace('\n', ' ')

        # print('game', game)

        # NOTE: there could be a bug on the en passant tracking
        # on game index 37, there apparently a pawn is being capture on passant
        # even though the pawn next to it in one direction (which is also
        # a friendly pawn) should not have the ability to captured on passant
        # the bug for game 37 is solved by double checking the color of the
        # pawn but we should take a look in the above comment

        p = PGN(game)

        # print('-' * 50)
        # print('pieces on board')

        pieces_on_board = p.game.board.pieces_on_board[PieceColor.BLACK]
        for key in pieces_on_board:
            print(
                key.name,
                [piece.algebraic_pos for piece in pieces_on_board[key]]
            )
        print('-' * 50)

        # black_king = p.game.board.get_piece(
        #     piece_name=PieceName.KING,
        #     color=PieceColor.BLACK
        # )[0]

        # print('legal moves for king', black_king.calculate_legal_moves(True))

        # for piece in PieceName.__members__.values():
        #     if pieces_on_board[piece]:
        #         print('-' * 50)
        #         print('piece_name', piece.name)
        #         p.game.board.print_attacked_squares(
        #             perspective=PieceColor.BLACK,
        #             traspass_king=True,
        #             show_in_algebraic_notation=True,
        #             piece_name=piece
        #         )
        #         print('-' * 50)
        # p.game.board.print_attacked_squares(
        #     perspective=PieceColor.BLACK,
        #     show_in_algebraic_notation=True
        # )

        p.game.board.print_board(show_in_algebraic_notation=True)

        print_success()


if __name__ == '__main__':
    unittest.main()
