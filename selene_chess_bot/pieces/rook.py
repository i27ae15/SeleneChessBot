from typing import TYPE_CHECKING

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

    def capture(self, captured_by: Piece):
        # eliminate the right to castle if the rook is captured
        self.board.castleling_rights[self.color][self.rook_side] = False
        return super().capture(captured_by)

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
            get_in_algebraic_notation=show_in_algebraic_notation
        )
        scanned_row = self.scan_row(
            king_color=king_color,
            end_at_piece_found=True,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares,
            get_in_algebraic_notation=show_in_algebraic_notation
        )

        legal_moves = list()

        # check if there is a capturable piece in the list of move
        if check_capturable_moves:
            legal_moves += self._check_capturable_moves(
                scanned_column['d0'],
                get_in_algebraic_notation=show_in_algebraic_notation
            )
            legal_moves += self._check_capturable_moves(
                scanned_column['d1'],
                get_in_algebraic_notation=show_in_algebraic_notation
            )

            legal_moves += self._check_capturable_moves(
                scanned_row['d0'],
                get_in_algebraic_notation=show_in_algebraic_notation
            )
            legal_moves += self._check_capturable_moves(
                scanned_row['d1'],
                get_in_algebraic_notation=show_in_algebraic_notation
            )
        else:
            legal_moves += self._piece_to_alg_position(scanned_column['d0'])
            legal_moves += self._piece_to_alg_position(scanned_column['d1'])

            legal_moves += self._piece_to_alg_position(scanned_row['d0'])
            legal_moves += self._piece_to_alg_position(scanned_row['d1'])

        return legal_moves

    def _piece_to_alg_position(
        self,
        moves: list[str | list[int, int]],
    ) -> str:
        if moves and isinstance(moves[-1], Piece):
            moves[-1] = moves[-1].algebraic_pos
        return moves

    def _validate_before_moving(self) -> None:

        """
        This will eliminate the right to castle if the rook is moved
        for the first time.
        """

        if self.first_move:
            self.board.castleling_rights[self.color][self.rook_side] = False
