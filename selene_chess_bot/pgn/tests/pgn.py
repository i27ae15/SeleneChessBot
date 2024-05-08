from django.test import TestCase

from pgn.pgn import PGN

from core.testing import print_starting, print_success


class TestPGN(TestCase):

    def extract_pgn_to_variables(self, file_path: str) -> list[str]:
        with open(file_path, 'r') as file:
            games = file.read().strip().split('\n\n')

        return games

    def test_pgn_string_format(self):

        print_starting()
        PGN('1.e4 e6 2.d4 d5 3.Nd2 Nf6')
        print_success()

    def test_pgn_dict_format(self):

        print_starting()
        PGN(
            {
                '1': ['e4', 'e6'],
                '2': ['d4', 'd5'],
                '3': ['Nd2', 'Nf6']
            }
        )
        print_success()

    def test_pgn_string_format_castleling(self):

        pgn = "1.d4 d5 2.Bf4 e6 3.e3 Nf6 4.Nd2 Bd6 5.Bg3 c6 6.c3 O-O 7.Qc2 Re8 8.O-O-O h6"

        print_starting()
        pgn = PGN(pgn)
        print(pgn.pgn)
        print_success()

    def test_pgn_from_real_games(self):

        print_starting()
        # Usage
        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)

        for index, game in enumerate(pgn_games):
            g = game.replace('\n', ' ')
            print('game', index + 1)
            PGN(g)
        print_success()

    def test_unique_game(self):

        print_starting()

        file_path = 'pgn/tests/MacKenzie.txt'
        pgn_games = self.extract_pgn_to_variables(file_path)
        game = pgn_games[1].replace('\n', ' ')

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


if __name__ == '__main__':
    unittest.main()

# state_parts = []

# # Castling rights
# for color, rights in self.board.castleling_rights.items():
#     color_prefix = "White" if color == PieceColor.WHITE else "Black"
#     castling = []
#     if rights[RookSide.KING]:
#         castling.append("O-O")
#     if rights[RookSide.QUEEN]:
#         castling.append("O-O-O")
#     state_parts.append(f"{color_prefix}_{'_'.join(castling)}" if castling else f"{color_prefix}_NoCastling")

# for color, pieces in self.board.pieces_on_board.items():
#     color_prefix = "White" if color == PieceColor.WHITE else "Black"
#     for piece_type, piece_list in pieces.items():
#         for piece in piece_list:
#             piece: Piece
#             # Directly use piece.row and piece.column
#             pos = f"{piece.column}{piece.row}"
#             state_parts.append(f"{piece_type.value[1]}{pos}")

# state = " - ".join(state_parts)

# if state in self.board_states:
#     st = self.board_states[state]
#     self.board_states[state] = st + 1
# else:
#     self.board_states[state] = 1