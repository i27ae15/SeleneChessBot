from collections.abc import Iterable
from typing import TypedDict

from dataclasses import dataclass


# ----------------- Type Aliases -----------------

PositionT = tuple[int, int]

# ----------------- Dataclasses -----------------


@dataclass
class Position:

    """
        A dataclass to represent a position in a 2D list
        with a row and a column

        row: int
        column: int
    """

    row: int
    column: int


@dataclass
class Row:
    row: list[str]

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

        List[Row * 8]

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

        Where the minuscule letters are the black pieces and the
        capital letters are the white pieces

        ### Important:
        This is just a type, is not necessary to use as a instance

        ### Note:
            - The empty square could also be represented by None or 0.
            - The pieces could be represented by Piece objects
    """

    def __init__(self, board: list[list[str]]):
        self.board = board

    def __iter__(self) -> Iterable[list[str]]:
        return iter(self.board)
