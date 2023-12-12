from pieces.pieces import Piece
from typing import TYPE_CHECKING
from .utilites import PieceColor, PieceValue, PieceName

if TYPE_CHECKING:
    from board import Board


class Knight(Piece):

    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        board: 'Board'
    ):
        super().__init__(
            color,
            position,
            value=PieceValue.KNIGHT,
            name=PieceName.KNIGHT,
            board=board
        )

    def move(self, new_position: tuple[int, int]):
        super().move(new_position)

    def can_move(self, new_position: tuple[int, int]) -> bool:
        return super().can_move(new_position)

    def calculate_legal_moves(self, board) -> list:
        return super().calculate_legal_moves(board)
