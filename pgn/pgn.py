from game import Game


class PGN:

    """
    This will be a class that will save the moves in a pgn format
    """

    def __init__(self, moves: str | dict) -> None:

        self.pgn: str = self.convert_to_pgn(moves)

    def convert_to_pgn(self, moves: str | dict) -> str:

        """
        This method will convert the moves to a pgn format.

        :param moves: The moves that will be converted to pgn
        :return: The moves in pgn format

        """

        if isinstance(moves, str):
            moves = self.check_if_pgn_is_valid(moves)

        if isinstance(moves, dict):
            moves = self.convert_dict_to_pgn(moves)

        return moves

    def check_if_pgn_is_valid(self, moves: str) -> str:
        """
        This method will check if the moves are in pgn format.

        :param moves: The moves that will be checked
        :return: The moves in pgn format

        The format of a valid PGN should look something like this:

        1. e4 e6
        2. d4 d5
        3. Nd2 Nf6
        4. e5 Nfd7
        ...
        1-0

        """

        # we want to create the game object and recreate these moves to
        # see if they are valid ones
        game: Game = Game()

        # cut the string in the dot
        splited_moves = moves.split('.')
        # eliminate the first element of the list
        # this looks horrible, we should make it more elegant
        splited_moves = splited_moves[1:]
        splited_moves[-1] = splited_moves[-1] + '0'

        for move in splited_moves:

            # we have to delete the last element of the move string
            # because of the way we split the string
            move = move[:-1]

            # now, we have to cut the string in two parts
            # the white move and the black move

            white_move, black_move = self._get_white_and_black_moves(move)

            # put the moves into the game and see if they are valid

            game.move_piece(white_move)
            game.move_piece(black_move)

        print(game.board.print_board())

        return moves

    def convert_dict_to_pgn(self, moves: dict) -> str:
        """
        This method will convert the moves from a dictionary to a pgn format.

        :param moves: The moves that will be converted
        :return: The moves in pgn format

        the dictionary will look like this:

        {
            1: ['e4', 'e6'],
            2: ['d4', 'd5'],
            3: ['Nd2', 'Nf6']
            ...
        }

        """

        # We have to convert the dictionary into a string

        pgn = str()

        # create a game object to validate the moves in the dictionary

        game = Game()

        for key in moves:

            white_move = moves[key][0]
            black_move = moves[key][1]

            game.move_piece(white_move)
            game.move_piece(black_move)

            pgn += f'{key}. {white_move} {black_move} '

        return pgn

    def _get_white_and_black_moves(self, move: str) -> tuple[str, str]:

        white_move = str()
        black_move = str()

        white_move, black_move = move.strip().split(' ')
        return white_move, black_move
