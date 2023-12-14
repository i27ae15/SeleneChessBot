from typing import TYPE_CHECKING

from core.utilities import convert_to_algebraic_notation
from pieces.piece import Piece

from .utilites import PieceColor, PieceValue, PieceName

if TYPE_CHECKING:
    from board import Board


class Bishop(Piece):

    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        board: 'Board'
    ):
        super().__init__(
            color,
            position,
            value=PieceValue.BISHOP,
            name=PieceName.BISHOP,
            board=board
        )

    def move(self, new_position: tuple[int, int]):
        super().move(new_position)

    def can_move(self, new_position: tuple[int, int]) -> bool:
        return super().can_move(new_position)

    def get_attacked_squares(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list[str | list[int]]:
        return self.calculate_legal_moves(
            show_in_algebraic_notation=show_in_algebraic_notation,
            check_capturable_moves=False
        )

    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        check_capturable_moves: bool = True
    ) -> list[str | list[int, int]]:

        diagonal_moves: list[list[int, int] | Piece] = self.scan_diagonals()
        legal_moves: list[list[int, int]] = []

        for key in diagonal_moves:
            if check_capturable_moves:
                legal_moves += self._check_capturable_moves(
                    diagonal_moves[key]
                )
            else:
                legal_moves += diagonal_moves[key]

        if show_in_algebraic_notation:
            algebraic_list = []
            for move in legal_moves:
                if isinstance(move, Piece):
                    move = move.position
                algebraic_list.append(convert_to_algebraic_notation(*move))
            return algebraic_list

        return legal_moves
