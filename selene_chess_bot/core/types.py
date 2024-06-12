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
