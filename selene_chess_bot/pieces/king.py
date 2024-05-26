from typing import TYPE_CHECKING

from core.utils import convert_to_algebraic_notation
from core.types import PositionT

from pieces.piece import Piece
from pieces.utilites import PieceColor, PieceValue, PieceName, RookSide


if TYPE_CHECKING:
    from board import Board


class King(Piece):

    # TODO: Not attacking square when another square is
    # attacked by the same square as the king

    def __init__(
        self,
        color: PieceColor,
        position: PositionT,
        board: 'Board'
    ):

        self.is_in_check: bool = False

        super().__init__(
            color,
            position,
            value=PieceValue.KING,
            name=PieceName.KING,
            board=board
        )

    @property
    def can_castle_kingside(self) -> bool:
        return self._check_if_kingside_castleling_is_possible()

    @property
    def can_castle_queenside(self) -> bool:
        return self._check_if_queenside_castleling_is_possible()

    @property
    def can_castle(self) -> bool:
        return self.can_castle_kingside or self.can_castle_queenside

    def check_if_in_check(self) -> bool:
        if self.get_pieces_attacking_me():
            self.is_in_check = True
        else:
            self.is_in_check = False

        return self.is_in_check

    def get_attacked_squares(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list[str | list[int]]:
        return self._calculate_legal_moves(
            show_in_algebraic_notation=show_in_algebraic_notation,
            check_capturable_moves=False,
            check_for_attacked_squares=False
        )

    def castle(
        self,
        side: RookSide
    ) -> bool:

        sides = {
            RookSide.KING: self._check_if_kingside_castleling_is_possible,
            RookSide.QUEEN: self._check_if_queenside_castleling_is_possible
        }

        if not sides[side]():
            return False

        rooks = self.board.get_piece(
            piece_name=PieceName.ROOK,
            color=self.color,
        )

        rook = [r for r in rooks if r.rook_side == side][0]

        # calculate the king direction based on the color and the side
        # of the castleling
        king_direction = 1 if side == RookSide.KING else -1
        rook_direction = 1 if side == RookSide.KING else -1

        # move the rook
        rook.move_to(
            new_position=(
                self.position[0],
                self.position[1] + 1 * rook_direction
            )
        )

        # move the king
        self.move_to(
            new_position=[
                self.position[0],
                self.position[1] + 2 * king_direction
            ],
            in_castleling=True
        )

        return True

    def _calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        check_capturable_moves: bool = True,
        check_for_attacked_squares: bool = True,
        **kwargs
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
            (self.position[0], self.position[1] + 1),
        ]

        legal_moves = []
        attacked_squares = self.board.get_attacked_squares(
            self.color.opposite(),
            traspass_king=True,
            show_in_algebraic_notation=False
        )

        for position in positions_to_check:
            if self.board.is_position_on_board(position):
                if not check_for_attacked_squares:
                    legal_moves.append(position)
                    continue
                if position not in attacked_squares:
                    if check_capturable_moves:
                        square = [
                            self.board.get_square_or_piece(
                                row=position[0],
                                column=position[1]
                            )
                        ]
                        legal_moves += self._check_capturable_moves(square)
                    else:
                        legal_moves.append(position)

        # check if possible to castle
        kingside_cas_pos = (self.position[0], self.position[1] + 2)
        if self._check_if_kingside_castleling_is_possible():
            legal_moves.append(kingside_cas_pos)

        queenside_cas_pos = (self.position[0], self.position[1] - 2)
        if self._check_if_queenside_castleling_is_possible():
            legal_moves.append(queenside_cas_pos)

        if show_in_algebraic_notation:
            for move in legal_moves:
                legal_moves[legal_moves.index(move)] = convert_to_algebraic_notation(
                    *move,
                    king_color=self.color,
                    can_castle=self.can_castle
                )

        return legal_moves

    def _check_if_queenside_castleling_is_possible(
        self
    ) -> bool:

        # check if the king has the right to castle
        if not self.board.castleling_rights[self.color][RookSide.QUEEN]:
            return False

        # check if the squares between the king and the rook are empty
        squares_to_check = [
            (self.position[0], self.position[1] - 1),
            (self.position[0], self.position[1] - 2),
            (self.position[0], self.position[1] - 3)
        ]

        return self._castleling_helper(
            multiplier=-1,
            squares_to_check=squares_to_check
        )

    def _check_if_kingside_castleling_is_possible(
        self
    ) -> bool:

        # check if the king has the right to castle
        if not self.board.castleling_rights[self.color][RookSide.KING]:
            return False

        # check if the squares between the king and the rook are empty
        squares_to_check = [
            (self.position[0], self.position[1] + 1),
            (self.position[0], self.position[1] + 2)
        ]

        return self._castleling_helper(
            multiplier=1,
            squares_to_check=squares_to_check
        )
    # ---------------------------- PRIVATE METHODS ----------------------------

    def _castleling_helper(
        self,
        multiplier: int,
        squares_to_check: list[PositionT],
    ) -> bool:

        for square in squares_to_check:
            if not self.board.is_position_empty(
                row=square[0],
                column=square[1]
            ):
                return False

        # check if the square the king is moving to is under attack
        attacked_squares = self.board.get_attacked_squares(
            self.color.opposite(),
            show_in_algebraic_notation=False
        )

        for i in range(len(squares_to_check), 0, -1):
            pos = (self.position[0], self.position[1] + (i * multiplier))
            if pos in attacked_squares:
                return False

        return True

    # ---------------------------- HELPER METHODS ----------------------------

    def _validate_before_moving(self):

        """
        This will delete the rights to clastle if the king is moved
        """

        if self.first_move:
            self.board.castleling_rights[self.color][RookSide.KING] = False
            self.board.castleling_rights[self.color][RookSide.QUEEN] = False
