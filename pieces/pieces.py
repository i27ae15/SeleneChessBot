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
