from collections.abc import Iterable
from typing import TypedDict, List


# ----------------- Type Aliases -----------------

Row = List[str]

# ----------------- Typed Dicts -----------------


class MoveDict(TypedDict):

    """

        Moves dict will look like this:

        {
            #N: [Move 1, Move 2]
        }

        Where the first element of the list if the move for white and the
        second for the black player

    """

    move_number: list[str, str]


class BoardStates(TypedDict):

    """
        A dictionary to save the states of the current game

        {
            "byte_state": "times_reached"
        }

    """

    bytes_obj: int


# ----------------- Classes -----------------


class BoardRepresentation():
    """
        Representates a board in a chess game in a
        8x8 2D list

        List[Row, Row]

        that could looks like this:

        [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],

            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],

            ['.', '.', '.', '.', '.', '.', '.', '.'],

            ['.', '.', '.', '.', '.', '.', '.', '.'],

            ['.', '.', '.', '.', '.', '.', '.', '.'],

            ['.', '.', '.', '.', '.', '.', '.', '.'],

            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],

            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    """

    def __init__(self, board: list[list[str]]):
        self.board = board

    def __iter__(self) -> Iterable[list[str]]:
        return iter(self.board)
