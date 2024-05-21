from typing import TYPE_CHECKING

from core.utils import convert_to_algebraic_notation
from core.types import PositionT

from .piece import Piece
from .utilites import PieceColor, PieceValue, PieceName


if TYPE_CHECKING:
    from board import Board


class Pawn(Piece):
    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        board: 'Board'
    ):

        # TODO: Add the x when capturing a piece

        self.can_be_captured_en_passant: bool = False
        self._legal_moves: list[PositionT] = []

        super().__init__(
            color,
            position,
            value=PieceValue.PAWN,
            name=PieceName.PAWN,
            board=board
        )

    def coronate(self, coronate_into: PieceName):

        self.board.remove_piece(self)
        self.board.add_piece(
            piece=coronate_into,
            piece_color=self.color,
            row=self.row,
            column=self.column
        )

    def get_attacked_squares(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list[tuple[int, int]]:
        # get the squares that are being under attacked by the pawn
        direction = 1 if self.color == PieceColor.WHITE else -1
        squares_being_attacked: list[tuple[int, int]] = []

        # get the left squared attacked by the pawn
        if self.position[1] - 1 >= 0:
            squares_being_attacked.append(
                (self.position[0] + 1 * direction, self.position[1] - 1)
            )

        # get the right squared attacked by the pawn
        if self.position[1] + 1 <= 7:
            squares_being_attacked.append(
                (self.position[0] + 1 * direction, self.position[1] + 1)
            )

        if show_in_algebraic_notation:
            return [
                convert_to_algebraic_notation(*square)
                for square in squares_being_attacked
            ]

        return squares_being_attacked

    def _calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        show_captuable_enpt: bool = False,
        **kwargs
    ) -> list[tuple[int, int]] | list[str]:

        direction = 1 if self.color == PieceColor.WHITE else -1
        self._legal_moves: list[PositionT] = []

        # Check if the pawn can move forward
        self._set_forward_moves(
            direction,
            show_in_algebraic_notation=show_in_algebraic_notation
        )
        self._set_capturable_moves(
            direction,
            show_in_algebraic_notation=show_in_algebraic_notation
        )
        self._set_en_passant_moves(
            show_in_algebraic_notation=show_in_algebraic_notation,
            show_capture_move=show_captuable_enpt
        )

        return self._legal_moves

    def _get_on_passant_square(self) -> tuple[int, int] | None:

        # the first things we need to check if whether we have a pawn
        # next to the left or to the right of this pawn

        # check if there is a pawn in direction 0
        direction = 1 if self.color == PieceColor.WHITE else -1
        if self.position[1] - 1 >= 0:
            piece: Piece | tuple = self.board.get_square_or_piece(
                row=self.position[0],
                column=self.position[1] - 1
            )
            if isinstance(piece, Pawn):
                if (
                    piece.color != self.color and
                    piece.can_be_captured_en_passant
                ):
                    return (
                        self.position[0] + 1 * direction, self.position[1] - 1
                    )

        # check if there is pawn in direction 1
        if self.position[1] + 1 <= 7:
            piece: Piece | tuple = self.board.get_square_or_piece(
                row=self.position[0],
                column=self.position[1] + 1
            )

            if isinstance(piece, Pawn):
                if (
                    piece.color != self.color and
                    piece.can_be_captured_en_passant
                ):
                    return (
                        self.position[0] + 1 * direction, self.position[1] + 1
                    )

        self.board.get_square_or_piece(row=self.position[0] - 1, column=0)

    def _set_en_passant_moves(
        self,
        show_in_algebraic_notation: bool,
        show_capture_move: bool = False
    ) -> None:
        en_passant_square = self._get_on_passant_square()
        if en_passant_square is not None:
            if show_in_algebraic_notation:
                en_passant_square = convert_to_algebraic_notation(
                    *en_passant_square
                )
            s = en_passant_square

            if show_capture_move:
                s = f'{self.algebraic_pos[0]}x{en_passant_square}'

            self._legal_moves.append(s)

    def _set_forward_moves(
        self,
        direction: int,
        show_in_algebraic_notation: bool
    ) -> None:

        can_move_forward: bool = False

        # Check if the pawn can move forward one square
        pos_to: PositionT = (
            self.position[0] + 1 * direction,
            self.position[1]
        )

        if self.board.is_position_empty(*pos_to):
            can_move_forward = True

            # check if the pawn can coronate and here the only option for the
            # moment is to add as algebraic notation
            if pos_to[0] == 0 or pos_to[0] == 7:
                pos_to = convert_to_algebraic_notation(*pos_to)
                self._legal_moves.append(f'{pos_to}=Q')
                self._legal_moves.append(f'{pos_to}=R')
                self._legal_moves.append(f'{pos_to}=N')
                self._legal_moves.append(f'{pos_to}=B')
                return

            if show_in_algebraic_notation:
                pos_to = convert_to_algebraic_notation(*pos_to)

            self._legal_moves.append(pos_to)

        # Check if the pawn can move forward two squares
        pos_to: tuple[int, int] = (
            self.position[0] + 2 * direction,
            self.position[1]
        )
        if self.first_move and can_move_forward:
            if self.board.is_position_empty(*pos_to):

                if show_in_algebraic_notation:
                    pos_to = convert_to_algebraic_notation(*pos_to)

                self._legal_moves.append(pos_to)

    def _set_capturable_moves(
        self,
        direction: int,
        show_in_algebraic_notation: bool
    ) -> None:

        board = self.board.board

        # Check if the pawn can capture a piece
        # check if the pawn can capture a piece on the left
        if self.position[1] - 1 >= 0:
            pos_to: tuple[int, int] = (
                self.position[0] + 1 * direction,
                self.position[1] - 1
            )

            piece: Piece | None = board[pos_to[0]][pos_to[1]]

            if piece is not None and piece.color != self.color:

                if self._set_capture_in_coronation(pos_to):
                    return

                if show_in_algebraic_notation:
                    pos_to = convert_to_algebraic_notation(*pos_to)

                self._legal_moves.append(pos_to)

        # check if the pawn can capture a piece on the right
        if self.position[1] + 1 <= 7:
            pos_to: tuple[int, int] = (
                self.position[0] + 1 * direction,
                self.position[1] + 1
            )

            piece: Piece | None = board[pos_to[0]][pos_to[1]]

            if piece is not None and piece.color != self.color:

                if self._set_capture_in_coronation(pos_to):
                    return

                if show_in_algebraic_notation:
                    pos_to = convert_to_algebraic_notation(*pos_to)
                    # the x

                self._legal_moves.append(pos_to)

    def _set_capture_in_coronation(self, pos_to: PositionT) -> bool:

        if pos_to[0] == 0 or pos_to[0] == 7:
            pos_to = convert_to_algebraic_notation(*pos_to)
            self._legal_moves.append(f'{self.algebraic_pos[0]}x{pos_to}=Q')
            self._legal_moves.append(f'{self.algebraic_pos[0]}x{pos_to}=R')
            self._legal_moves.append(f'{self.algebraic_pos[0]}x{pos_to}=N')
            self._legal_moves.append(f'{self.algebraic_pos[0]}x{pos_to}=B')
            return True

        return False
