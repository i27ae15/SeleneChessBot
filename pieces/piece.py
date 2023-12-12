from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.utilities import convert_to_algebraic_notation

from .utilites import PieceColor, PieceValue, PieceName

if TYPE_CHECKING:
    from board import Board


class Piece(ABC):
    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        value: PieceValue,
        name: PieceName,
        board: 'Board'
    ):
        self.color: PieceColor = color
        self.value: PieceValue = value

        self.position: tuple[int, int] = position
        self.move_story: list[tuple[int, tuple[int, int]]] = []
        self.first_move: bool = True
        self.captured_by: Piece | None = None
        self.name: PieceName = name
        self.board: 'Board' = board  # Class Board in board.py

    @property
    def is_captured(self) -> bool:
        return True if self.captured_by is not None else False

    @property
    def algebraic_pos(self) -> str:
        return convert_to_algebraic_notation(*self.position)

    @property
    def row(self) -> int:
        return self.position[0]

    @property
    def column(self) -> int:
        return self.position[1]

    @property
    def sing_char(self) -> str:
        return self.name.value[1]

    def capture(self, captured_by: 'Piece'):
        self.captured_by = captured_by

    def move(self, new_position: tuple[int, int]):
        self.position = new_position
        if self.first_move:
            self.first_move = False

    def add_move_to_story(
        self,
        move_number: int,
        new_position: tuple[int, int]
    ):
        self.move_story.append((move_number, new_position))

    def undo_move(self):
        if self.move_story:
            move_number, last_position = self.move_story.pop()
            self.position = last_position
            if move_number == 1:
                self.first_move = True

    def scan_column(self, end_at_piece_found: bool = True) -> dict:

        """

        This instance will scan the column where the piece is located and
        until it finds another piece or the end of the board.

        The function will return a dictionary with the following structure:

        {
            '0': [[int, int] | [Pieces]],
            '1': [[int, int] | [Pieces]]
        }

        Where the [int, int] is the position of the square and [Pieces] is a
        list of the pieces found in the column.

        """

        board = self.board.board
        squares_up: list[Piece | None] = []
        squares_down: list[Piece | None] = []

        # check the column in one direction
        for row in range(self.row - 1, -1, -1):
            if board[row][self.column] is None:
                squares_up.append([row, self.column])
            else:
                squares_up.append(board[row][self.column])
                if end_at_piece_found:
                    break

        # check the column in another direction
        for row in range(self.row + 1, 8):
            if board[row][self.column] is None:
                squares_down.append([row, self.column])
            else:
                squares_down.append(board[row][self.column])
                if end_at_piece_found:
                    break

        return {
            '0': squares_up,
            '1': squares_down
        }

    def scan_row(self, end_at_piece_found: bool = True) -> dict:

        """

        This instance will scan the row where the piece is located and
        until it finds another piece or the end of the board.

        The function will return a dictionary with the following structure:

        {
            '0': [[int, int] | [Pieces]],
            '1': [[int, int] | [Pieces]]
        }

        Where the [int, int] is the position of the square and [Pieces] is a
        list of the pieces found in the row.

        """

        board = self.board.board
        squares_left: list[Piece | None] = []
        squares_right: list[Piece | None] = []

        # check the row in one direction
        for column in range(self.column - 1, -1, -1):
            if board[self.row][column] is None:
                squares_left.append([self.row, column])
            else:
                squares_left.append(board[self.row][column])
                if end_at_piece_found:
                    break

        # check the row in another direction
        for column in range(self.column + 1, 8):
            if board[self.row][column] is None:
                squares_right.append([self.row, column])
            else:
                squares_right.append(board[self.row][column])
                if end_at_piece_found:
                    break

        return {
            '0': squares_left,
            '1': squares_right
        }

    @abstractmethod
    def can_move(self, new_position: tuple[int, int]) -> bool:
        pass

    @abstractmethod
    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list[tuple[int, int]] | list[str]:
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self.color}, {self.position})"
