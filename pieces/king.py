from typing import TYPE_CHECKING

from core.utilities import convert_to_algebraic_notation
from pieces.piece import Piece

from .utilites import PieceColor, PieceValue, PieceName

if TYPE_CHECKING:
    from board import Board


class King(Piece):

    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        board: 'Board'
    ):
        super().__init__(
            color,
            position,
            value=PieceValue.KING,
            name=PieceName.KING,
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
            check_capturable_moves=False
        )

    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        check_capturable_moves: bool = True
    ) -> list[str | list[int, int]]:

        # The king is special, because it can only move if a piece is not
        # attacking the square it wants to move to. So, we need to check
        # if the square is under attack by the opposite color.

        positions_to_check = [
            (self.position[0] + 1, self.position[1] + 1),
            (self.position[0] + 1, self.position[1]),
            (self.position[0] + 1, self.position[1] - 1),
            (self.position[0], self.position[1] - 1),
            (self.position[0] - 1, self.position[1] - 1),
            (self.position[0] - 1, self.position[1]),
            (self.position[0] - 1, self.position[1] + 1),
            (self.position[0], self.position[1] + 1)
        ]

        legal_moves = []
        attacked_squares = self.board.get_attacked_squares(
            self.color.opposite(),
            show_in_algebraic_notation=False
        )

        for position in positions_to_check:
            if self.board.is_position_on_board(position):
                if check_capturable_moves:
                    if position not in attacked_squares:
                        square = [
                            self.board.get_square_or_piece(
                                row=position[0],
                                column=position[1]
                            )
                        ]
                    legal_moves += self._check_capturable_moves(square)
                else:
                    legal_moves.append(position)

        if show_in_algebraic_notation:
            return [
                convert_to_algebraic_notation(*move) for move in legal_moves
            ]

        return legal_moves
