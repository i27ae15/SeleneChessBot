from typing import TYPE_CHECKING

from core.utilities import convert_to_algebraic_notation
from pieces.piece import Piece

from .utilites import PieceColor, PieceValue, PieceName

if TYPE_CHECKING:
    from board import Board


class Rook(Piece):

    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        board: 'Board'
    ):
        super().__init__(
            color,
            position,
            value=PieceValue.ROOK,
            name=PieceName.ROOK,
            board=board
        )

    def move(self, new_position: tuple[int, int]):
        super().move(new_position)

    def can_move(self, new_position: tuple[int, int]) -> bool:
        return super().can_move(new_position)

    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list[str | list[int, int]]:

        scanned_column = self.scan_column(end_at_piece_found=True)
        scanned_row = self.scan_row(end_at_piece_found=True)

        legal_moves = list()

        # check if there is a capturable piece in the list of move

        legal_moves += self._check_capturable_moves(scanned_column['d0'])
        legal_moves += self._check_capturable_moves(scanned_column['d1'])

        legal_moves += self._check_capturable_moves(scanned_row['d0'])
        legal_moves += self._check_capturable_moves(scanned_row['d1'])

        if show_in_algebraic_notation:
            return [
                convert_to_algebraic_notation(*move) for move in legal_moves
            ]

        return legal_moves
