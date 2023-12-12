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

    def _check_moves_list(
        self,
        moves: list[list[int, int] | Piece]
    ) -> list[list[int, int] | Piece]:

        if not len(moves):
            return moves

        if isinstance(moves[-1], Piece):
            is_capturable = True
            if moves[-1].color == self.color:
                is_capturable = False
                moves.pop()

            if is_capturable:
                moves[-1] = moves[-1].position
        return moves

    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list:

        column_moves: list[list[int, int] | Piece] = []
        row_moves: list[list[int, int] | Piece] = []

        scanned_column = self.scan_column(end_at_piece_found=True)
        scanned_row = self.scan_row(end_at_piece_found=True)

        column_moves = list()
        row_moves = list()

        # check if there is a capturable piece in the list of move

        column_moves += self._check_moves_list(scanned_column['d0'])
        column_moves += self._check_moves_list(scanned_column['d1'])

        row_moves += self._check_moves_list(scanned_row['d0'])
        row_moves += self._check_moves_list(scanned_row['d1'])

        legal_moves = column_moves + row_moves

        if show_in_algebraic_notation:
            return [
                convert_to_algebraic_notation(*move) for move in legal_moves
            ]

        return legal_moves
