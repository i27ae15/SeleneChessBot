from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.utilities import (
    convert_from_algebraic_notation, convert_to_algebraic_notation
)

from .utilites import PieceColor, PieceValue, PieceName, RookSide

if TYPE_CHECKING:
    from board import Board


class Piece(ABC):
    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        value: PieceValue,
        name: PieceName,
        board: 'Board'
    ):
        self.color: PieceColor = color
        self.value: PieceValue = value

        self.position: tuple[int, int] = position
        self.move_story: list[tuple[int, tuple[int, int]]] = []
        self.first_move: bool = True
        self.captured_by: Piece | None = None
        self.name: PieceName = name
        self.board: 'Board' = board

    @property
    def is_captured(self) -> bool:
        return True if self.captured_by is not None else False

    @property
    def algebraic_pos(self) -> str:
        return convert_to_algebraic_notation(*self.position)

    @property
    def row(self) -> int:
        return self.position[0]

    @property
    def column(self) -> int:
        return self.position[1]

    @property
    def sing_char(self) -> str:
        return self.name.value[1]

    def _check_capturable_moves(
        self,
        moves: 'list[list[int, int], Piece | Piece]',
        check_only_last_move: bool = True
    ) -> list[list[int, int]]:

        """
        Filter and modify a list of moves to only include capturable moves.

        This method processes a list of moves and checks for the presence
        of an enemy piece at the end of the move sequence. If the last move is
        a capturable enemy piece, it is replaced with its position. If the
        last move is not capturable (either an ally piece or an empty square),
        it is removed from the list.

        Parameters:
        moves (list[list[int, int] | Piece]): A list of moves, where each move
        is represented either as coordinates or a Piece object.

        check_only_last_move (bool): If True, only the last move in the list
        will be checked for capturability. If False, all moves in the list will
        be checked.

        Returns:
        list[list[int, int]]: A list of moves after filtering and modifying to
        include only capturable moves. Each move is represented as a list of
        coordinates.
        """

        if not len(moves):
            return moves

        if check_only_last_move:
            if isinstance(moves[-1], Piece):
                is_capturable = True
                if moves[-1].color == self.color:
                    is_capturable = False
                    moves.pop()

                if is_capturable:
                    moves[-1] = tuple(moves[-1].position)
        else:
            for index, move in enumerate(moves):
                if isinstance(move, Piece):
                    is_capturable = True
                    if move.color == self.color:
                        is_capturable = False
                        moves.pop(index)

                    if is_capturable:
                        moves[index] = tuple(move.position)
        return moves

    def capture(self, captured_by: 'Piece'):
        self.captured_by = captured_by

    def move_to(
        self,
        new_position: tuple[int, int] | str,
    ):
        """
        Move the chess piece to a new position on the board.

        This method moves the piece to a specified position, which can be
        given either as a tuple of coordinates or as a string in algebraic
        notation. If the piece being moved is a rook or a king and it's their
        first move, the method adjusts the castling rights accordingly. For a
        rook, it disables castling on the rook's side. For a king, it disables
        castling on both the king and queen sides. The method checks if the
        move is legal before executing it and updates the board and the
        piece's position. It also marks the first move of the piece as
        completed.

        Parameters:
        new_position (tuple[int, int] | str): The new position to move the
        piece to, either as a tuple of coordinates (row, column)
        or a string in algebraic notation.

        Returns:
        bool: True if the move is successful and legal, False otherwise.

        Notes:
        - The method checks and updates castling rights if the piece is a rook
        or king moving for the first time.
        - The legality of the move is determined by the `calculate_legal_moves`
        method of the piece.
        """
        # check if is a rook and eliminate the right to castle
        if self.first_move and self.name == PieceName.ROOK:
            self.board.castleling_rights[self.color][self.rook_side] = False

        # check if is a king and eliminate the right to castle
        if self.first_move and self.name == PieceName.KING:
            self.board.castleling_rights[self.color][RookSide.KING] = False
            self.board.castleling_rights[self.color][RookSide.QUEEN] = False

        if isinstance(new_position, str):
            new_position = convert_from_algebraic_notation(new_position)

        if new_position in self.calculate_legal_moves():
            self.board.update_board(
                new_row=new_position[0],
                new_column=new_position[1],
                old_column=self.column,
                old_row=self.row,
                piece=self,
            )
            self.position = new_position

            self.first_move = False
            return True

        return False

    def add_move_to_story(
        self,
        move_number: int,
        new_position: tuple[int, int]
    ):
        self.move_story.append((move_number, new_position))

    def undo_move(self):
        if self.move_story:
            move_number, last_position = self.move_story.pop()
            self.position = last_position
            if move_number == 1:
                self.first_move = True

    def scan_column(self, end_at_piece_found: bool = True) -> dict:

        """
        This instance will scan the column where the piece is located and
        until it finds another piece or the end of the board.

        The function will return a dictionary with the following structure:

        {
            'd0': [[int, int] | [Pieces]],
            'd1': [[int, int] | [Pieces]]
        }

        Where the [int, int] is the position of the square and [Pieces] is a
        list of the pieces found in the column.

        """

        direction_0: list[Piece | None] = []
        direction_1: list[Piece | None] = []

        # check the column in one direction
        for row in range(self.row - 1, -1, -1):
            direction_0.append(
                self.board.get_square_or_piece(row, self.column)
            )
            if isinstance(direction_0[-1], Piece) and end_at_piece_found:
                break

        # check the column in another direction
        for row in range(self.row + 1, 8):
            direction_1.append(
                self.board.get_square_or_piece(row, self.column)
            )
            if isinstance(direction_1[-1], Piece) and end_at_piece_found:
                break

        return {
            'd0': direction_0,
            'd1': direction_1
        }

    def scan_row(self, end_at_piece_found: bool = True) -> dict:

        """
        This instance will scan the row where the piece is located and
        until it finds another piece or the end of the board.

        The function will return a dictionary with the following structure:

        {
            'd0': [[int, int] | [Pieces]],
            'd1': [[int, int] | [Pieces]]
        }

        Where the [int, int] is the position of the square and [Pieces] is a
        list of the pieces found in the row.

        """

        board = self.board.board
        squares_left: list[Piece | None] = []
        squares_right: list[Piece | None] = []

        # check the row in one direction
        for column in range(self.column - 1, -1, -1):
            if board[self.row][column] is None:
                squares_left.append([self.row, column])
            else:
                squares_left.append(board[self.row][column])
                if end_at_piece_found:
                    break

        # check the row in another direction
        for column in range(self.column + 1, 8):
            if board[self.row][column] is None:
                squares_right.append([self.row, column])
            else:
                squares_right.append(board[self.row][column])
                if end_at_piece_found:
                    break

        return {
            'd0': squares_left,
            'd1': squares_right
        }

    def scan_diagonals(self, end_at_piece_found: bool = True) -> dict:

        """
        This instance will scan the diagonals where the piece is located and
        until it finds another piece or the end of the board.

        The function will return a dictionary with the following structure:

        {
            'd0': [[int, int] | [Pieces]],
            'd1': [[int, int] | [Pieces]],
            'd2': [[int, int] | [Pieces]],
            'd3': [[int, int] | [Pieces]]
        }

        Where the [int, int] is the position of the square and [Pieces] is a

        """

        direction_0: list[Piece | None] = []
        direction_1: list[Piece | None] = []
        direction_2: list[Piece | None] = []
        direction_3: list[Piece | None] = []

        # check the up left diagonal
        for row, column in zip(
            range(self.row - 1, -1, -1),
            range(self.column - 1, -1, -1)
        ):
            direction_0.append(self.board.get_square_or_piece(row, column))
            if isinstance(direction_0[-1], Piece) and end_at_piece_found:
                break

        # check the up right diagonal
        for row, column in zip(
            range(self.row - 1, -1, -1),
            range(self.column + 1, 8)
        ):
            direction_1.append(self.board.get_square_or_piece(row, column))
            if isinstance(direction_1[-1], Piece) and end_at_piece_found:
                break

        # check the down left diagonal
        for row, column in zip(
            range(self.row + 1, 8),
            range(self.column - 1, -1, -1)
        ):
            direction_2.append(self.board.get_square_or_piece(row, column))
            if isinstance(direction_2[-1], Piece) and end_at_piece_found:
                break

        # check the down right diagonal
        for row, column in zip(
            range(self.row + 1, 8),
            range(self.column + 1, 8)
        ):
            direction_3.append(self.board.get_square_or_piece(row, column))
            if isinstance(direction_3[-1], Piece) and end_at_piece_found:
                break

        return {
            'd0': direction_0,
            'd1': direction_1,
            'd2': direction_2,
            'd3': direction_3
        }

    @abstractmethod
    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        check_capturable_moves: bool = True
    ) -> list[str | list[int, int]]:

        """
        Returns a list of legal moves for the piece.

        Parameters:
            show_in_algebraic_notation (bool): If True, returns the list of
            moves in algebraic notation. Defaults to False.
        """
        pass

    @abstractmethod
    def get_attacked_squares(
        self,
        show_in_algebraic_notation: bool = False
    ) -> list[str | list[int, int]]:
        """
        Return a list of the squares attacked by the piece.

        parameters:
            show_in_algebraic_notation (bool): If True, returns the list of
            moves in algebraic notation. Defaults to False.
        """
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self.color}, {self.position})"
