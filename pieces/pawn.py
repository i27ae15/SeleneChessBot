from typing import TYPE_CHECKING

from core.utils import convert_to_algebraic_notation

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

        self.can_be_captured_en_passant: bool = False

        super().__init__(
            color,
            position,
            value=PieceValue.PAWN,
            name=PieceName.PAWN,
            board=board
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

    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list[tuple[int, int]] | list[str]:

        board = self.board.board

        direction = 1 if self.color == PieceColor.WHITE else -1
        legal_moves: list[tuple[int, int]] = []

        can_move_forward: bool = False

        # Check if the pawn can move forward one square
        pos_to: tuple[int, int] = (
            self.position[0] + 1 * direction,
            self.position[1]
        )

        if self.board.is_position_empty(*pos_to):
            can_move_forward = True
            legal_moves.append(pos_to)

        # Check if the pawn can move forward two squares
        pos_to: tuple[int, int] = (
            self.position[0] + 2 * direction,
            self.position[1]
        )
        if self.first_move and can_move_forward:
            if self.board.is_position_empty(*pos_to):
                legal_moves.append(pos_to)

        # Check if the pawn can capture a piece
        # check if the pawn can capture a piece on the left
        if self.position[1] - 1 >= 0:
            pos_to: tuple[int, int] = (
                self.position[0] + 1 * direction,
                self.position[1] - 1
            )

            piece: Piece | None = board[pos_to[0]][pos_to[1]]

            if piece is not None and piece.color != self.color:
                legal_moves.append(pos_to)

        # check if the pawn can capture a piece on the right
        if self.position[1] + 1 <= 7:
            pos_to: tuple[int, int] = (
                self.position[0] + 1 * direction,
                self.position[1] + 1
            )

            piece: Piece | None = board[pos_to[0]][pos_to[1]]

            if piece is not None and piece.color != self.color:
                legal_moves.append(pos_to)

        # check if can en passant
        # check if the pawn can capture a piece on the left

        en_passant_square = self._get_on_passant_square()
        if en_passant_square is not None:
            legal_moves.append(en_passant_square)

        if show_in_algebraic_notation:
            return [
                convert_to_algebraic_notation(*move) for move in legal_moves
            ]

        return legal_moves

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
