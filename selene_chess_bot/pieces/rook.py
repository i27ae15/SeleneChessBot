from typing import TYPE_CHECKING

from core.utils import convert_to_algebraic_notation
from pieces.piece import Piece

from .utilites import PieceColor, PieceValue, PieceName, RookSide

if TYPE_CHECKING:
    from board import Board


class Rook(Piece):

    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        board: 'Board',
        rook_side: RookSide = None,
    ):

        self.rook_side: RookSide = rook_side

        super().__init__(
            color,
            position,
            value=PieceValue.ROOK,
            name=PieceName.ROOK,
            board=board
        )

    def get_attacked_squares(
        self,
        traspass_king: bool = False,
        king_color: PieceColor = None,
        show_in_algebraic_notation: bool = False
    ) -> list[str | list[int]]:
        return self._calculate_legal_moves(
            show_in_algebraic_notation=show_in_algebraic_notation,
            check_capturable_moves=False,
            traspass_king=traspass_king,
            king_color=king_color,
            get_only_squares=True
        )

    def _calculate_legal_moves(
        self,
        traspass_king: bool = False,
        king_color: PieceColor = None,
        get_only_squares: bool = False,
        check_capturable_moves: bool = True,
        show_in_algebraic_notation: bool = False,
        **kwargs
    ) -> list[str | list[int, int]]:

        scanned_column = self.scan_column(
            king_color=king_color,
            end_at_piece_found=True,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares,
        )
        scanned_row = self.scan_row(
            king_color=king_color,
            end_at_piece_found=True,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares
        )

        legal_moves = list()

        # check if there is a capturable piece in the list of move
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
