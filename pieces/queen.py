from typing import TYPE_CHECKING

from core.utilities import convert_to_algebraic_notation
from pieces.piece import Piece

from .utilites import PieceColor, PieceValue, PieceName

if TYPE_CHECKING:
    from board import Board


class Queen(Piece):

    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        board: 'Board'
    ):
        super().__init__(
            color,
            position,
            value=PieceValue.QUEEN,
            name=PieceName.QUEEN,
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

        # for the queen we got to combine the legal moves of the rook and the
        # bishop

        # first scan the diagonals
        legal_moves: list[list[int, int]] = []
        diagonal_moves: list[list[int, int] | Piece] = self.scan_diagonals()

        for key in diagonal_moves:
            legal_moves += self._check_capturable_moves(diagonal_moves[key])

        # now check for the legal moves of the rook
        scanned_column = self.scan_column(end_at_piece_found=True)
        scanned_row = self.scan_row(end_at_piece_found=True)

        legal_moves += self._check_capturable_moves(scanned_column['d0'])
        legal_moves += self._check_capturable_moves(scanned_column['d1'])

        legal_moves += self._check_capturable_moves(scanned_row['d0'])
        legal_moves += self._check_capturable_moves(scanned_row['d1'])

        if show_in_algebraic_notation:
            return [
                convert_to_algebraic_notation(*move) for move in legal_moves
            ]

        return legal_moves
