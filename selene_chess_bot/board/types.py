from dataclasses import dataclass

from collections.abc import Iterable


@dataclass
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
        In some parts of the code, this is being used just as a type

        ### Note:
            - The empty square could also be represented by None or 0.
            - The pieces could be represented by Piece objects
    """
    board: list[list[str]]

    def __iter__(self) -> Iterable[list[str]]:
        return iter(self.board)


@dataclass
class BoardStates:
    """
    A class to save the states of the current game

    Attributes:
        bytes_obj: The number of times a particular byte state has been
        reached.
    """
    bytes_obj: int
