from game.game import Game

from pieces.utilites import PieceColor

from core.debugger import debug_before_move_decorator, debug_at_end_of_moves


class PGN:

    """
    A class for handling and converting chess moves into Portable Game
    Notation (PGN).

    This class is responsible for converting a series of chess moves, provided
    either as a string or a dictionary, into PGN format. It includes methods
    to validate PGN strings and convert move dictionaries into PGN strings.

    Attributes:
        game (Game): An instance of the Game class to manage the chess game
        state.

        pgn (str): The PGN representation of the chess moves.

    Methods:
        convert_to_pgn(moves): Converts the given moves into PGN format.

        check_if_pgn_is_valid(moves): Validates if the provided PGN string is
        correctly formatted.

        convert_dict_to_pgn(moves): Converts a dictionary of moves into PGN
        format.

        _get_white_and_black_moves(move): Splits a move string into white and
        black moves.

    Example of PGN format:
        1. e4 e5 2. Nf3 Nc6 ...

    Example of move dictionary:
        {
            1: ['e4', 'e5'],
            2: ['Nf3', 'Nc6'],
            ...
        }
    """

    def __init__(self, moves: str | dict, debug: bool = False) -> None:
        """
        Initializes the PGN instance by setting up the game state and
        converting the provided moves into PGN format.

        :param moves: Chess moves in either string or dictionary format.

        :param debug: If true, the pgn will enter in a debuggin format
        where more things could be controlled in the console.

        """

        self.game: Game = Game()
        self.debug: bool = debug
        self._wait_for_move: int = False
        self.raw_moves: str | dict = moves
        self.pgn: str = self.convert_to_pgn(moves)

    def convert_to_pgn(self, moves: str | dict) -> str:
        """
        Converts the given moves into PGN format. Accepts either a string or a
        dictionary representation of moves and returns a PGN-formatted string.

        :param moves: Moves to be converted, either as a string or a
        dictionary.

        :return: A string representing the moves in PGN format.
        """

        if isinstance(moves, str):
            moves = self.check_if_pgn_is_valid(moves)

        if isinstance(moves, dict):
            moves = self.convert_dict_to_pgn(moves)

        return moves

    def check_if_pgn_is_valid(self, moves: str) -> str:
        """
        Checks and validates if the given PGN string is correctly formatted.
        The method verifies each move within the string to ensure it adheres
        to PGN standards.

        :param moves: A string representing the moves in PGN format to be
        validated.

        :return: The original PGN string if valid.
        """

        # we want to create the game object and recreate these moves to
        # see if they are valid ones
        splited_moves = moves.split('.')
        # eliminate the first element of the list
        # this looks horrible, we should make it more elegant
        splited_moves = splited_moves[1:]

        is_valid_pgn = True

        for index, move in enumerate(splited_moves):

            # now, we have to cut the string in two parts
            # the white move and the black move
            white_move, black_move = self._get_white_and_black_moves(move)

            if self.debug:
                _str = f'{index + 1}. {white_move} {black_move}'
                print(_str)

            current_moves = [white_move, black_move]
            color = [PieceColor.WHITE, PieceColor.BLACK]

            for i, move in enumerate(current_moves):
                if not move:
                    continue
                executed, message = self._execute_move_with_debug(
                    move,
                    color[i]
                )

                if not executed:
                    is_valid_pgn = False
                    if message:
                        print(message)
                    else:
                        message = ['White', 'Black']
                        print(
                            f'{message[i]} move not valid:',
                            current_moves[i],
                            'at move number', index + 1
                        )
                    break

            if not is_valid_pgn:
                break

        if self.debug:
            if is_valid_pgn:
                print('PGN is valid')
            if not is_valid_pgn:
                print('PGN is not valid')
                print('pgn', self.raw_moves)
            print('Press enter to finish or write a command ')
            debug_at_end_of_moves(self)

        return moves

    def convert_dict_to_pgn(self, moves: dict) -> str:
        """
        Converts a dictionary of moves into a PGN-formatted string. Each entry
        in the dictionary represents a turn with a pair of moves for white and
        black.

        :param moves: A dictionary where keys are move numbers and values are
        lists of white and black moves.

        :return: A string representing the moves in PGN format.
        """

        # We have to convert the dictionary into a string

        pgn = str()

        for key in moves:

            white_move = moves[key][0]
            black_move = moves[key][1]

            self.game.move_piece(white_move)
            self.game.move_piece(black_move)

            pgn += f'{key}. {white_move} {black_move} '

        return pgn

    def _get_white_and_black_moves(self, move: str) -> tuple[str, str]:
        """
        Splits a move string into separate white and black moves.

        :param move: A string containing both white and black moves.

        :return: A tuple containing separate strings for white and black
        moves.
        """

        white_move = str()
        black_move = str()

        try:
            stripped_move = move.split(' ')
            white_move = stripped_move[0]

            if len(stripped_move) > 1:
                black_move = stripped_move[1]

        except ValueError:
            print('error in move', move)

        return white_move, black_move

    @debug_before_move_decorator
    def _execute_move_with_debug(self, move: str, *args) -> bool:
        try:
            self.game.move_piece(move)
            return True, None
        except ValueError:
            return False, None
        except IndexError:

            str_error = """
                Index error, probably because the PGN as string has been
                passed with the moves separated by a space between the
                move number and the move itself.

                Wrong way:
                1. e4 e5 2. Nf3 Nc6

                Correct way:
                1.e4 e5 2.Nf3 Nc6
            """

            return False, str_error
