from core.utilities import convert_to_algebraic_notation

from .pieces import Piece
from .utilites import PieceColor, PieceValue, PieceName

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board


class Pawn(Piece):
    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        board: 'Board'
    ):
        super().__init__(
            color,
            position,
            value=PieceValue.PAWN,
            name=PieceName.PAWN,
            board=board
        )

    def move(self, new_position: tuple[int, int]):
        # check if the move is valid

        if new_position in self.calculate_legal_moves(self.board):
            # self.first_move = False
            return True

        # Implement pawn movement logic here
        super().move(new_position)

    def can_move(self, new_position):
        # Implement pawn movement logic here
        return super().can_move(new_position)

    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list[tuple[int, int]] | list[str]:
        """
        Use a search algorithm to find all the legal moves for the pawn.

        Rules for the pawn, can move one square forward, or two squares forward
        if it is the first move. Can only move diagonally if it is capturing
        another piece.

        :param board: The board object
        :return: A list of legal moves
        """
        # Check if is first move and just add the two forward moves

        board = self.board.board

        direction = 1 if self.color == PieceColor.WHITE else -1
        legal_moves: list[list[int, int]] = []

        can_move_forward: bool = False

        # Check if the pawn can move forward one square
        pos_to: tuple[int, int] = (
            self.position[0] + 1 * direction,
            self.position[1]
        )

        if board[pos_to[0]][pos_to[1]] is None:
            legal_moves.append(pos_to)
            can_move_forward = True

        # Check if the pawn can move forward two squares
        pos_to: tuple[int, int] = (
            self.position[0] + 2 * direction,
            self.position[1]
        )
        if self.first_move and can_move_forward:
            if board[pos_to[0]][pos_to[1]] is None:
                legal_moves.append(pos_to)

        # Check if the pawn can capture a piece
        # check if the pan can capture a piece on the left
        if self.position[1] - 1 >= 0:
            pos_to: tuple[int, int] = (
                self.position[0] + 1 * direction,
                self.position[1] - 1
            )

            piece: Piece | None = board[pos_to[0]][pos_to[1]]

            if piece is not None and piece.color != self.color:
                legal_moves.append(pos_to)

        # check if the pan can capture a piece on the right
        if self.position[1] + 1 <= 7:
            pos_to: tuple[int, int] = (
                self.position[0] + 1 * direction,
                self.position[1] + 1
            )

            piece: Piece | None = board[pos_to[0]][pos_to[1]]

            if piece is not None and piece.color != self.color:
                legal_moves.append(pos_to)

        if show_in_algebraic_notation:
            return [
                convert_to_algebraic_notation(*move) for move in legal_moves
            ]

        return legal_moves
