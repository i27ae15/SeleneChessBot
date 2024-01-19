from typing import TYPE_CHECKING

from core.utils import convert_to_algebraic_notation
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

    def get_attacked_squares(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list[str | list[int]]:
        return self.calculate_legal_moves(
            show_in_algebraic_notation=show_in_algebraic_notation,
            get_only_squares=True,
            traspase_king=True,
        )

    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        check_capturable_moves: bool = True,
        traspase_king: bool = False,
        get_only_squares: bool = False
    ) -> list[str | list[int, int]]:

        # for the queen we got to combine the legal moves of the rook and the
        # bishop

        # first scan the diagonals
        legal_moves: list[list[int, int]] = []
        diagonal_moves: list[list[int, int] | Piece] = self.scan_diagonals(
            end_at_piece_found=True,
            traspase_king=traspase_king,
            get_only_squares=get_only_squares
        )

        for key in diagonal_moves:
            if check_capturable_moves:
                legal_moves += self._check_capturable_moves(
                    diagonal_moves[key]
                )
            else:
                legal_moves += diagonal_moves[key]

        # now check for the legal moves of the rook
        scanned_column = self.scan_column(
            end_at_piece_found=True,
            get_only_squares=get_only_squares
        )
        scanned_row = self.scan_row(
            end_at_piece_found=True,
            get_only_squares=get_only_squares
        )

        if check_capturable_moves:
            legal_moves += self._check_capturable_moves(scanned_column['d0'])
            legal_moves += self._check_capturable_moves(scanned_column['d1'])

            legal_moves += self._check_capturable_moves(scanned_row['d0'])
            legal_moves += self._check_capturable_moves(scanned_row['d1'])

        else:
            legal_moves += scanned_column['d0']
            legal_moves += scanned_column['d1']

            legal_moves += scanned_row['d0']
            legal_moves += scanned_row['d1']

        if show_in_algebraic_notation:
            algebraic_list = []
            for move in legal_moves:
                if isinstance(move, Piece):
                    move = move.position
                algebraic_list.append(convert_to_algebraic_notation(*move))
            return algebraic_list

        return legal_moves
