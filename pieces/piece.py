from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.utils import (
    convert_from_algebraic_notation, convert_to_algebraic_notation
)

from .utilites import PieceColor, PieceValue, PieceName, RookSide

if TYPE_CHECKING:
    from board import Board


class Piece(ABC):

    """
    An abstract base class representing a generic chess piece on a chessboard.

    This class provides a template for all specific types of chess pieces
    (e.g., Pawn, Rook, Knight, etc.) and includes common attributes and methods
    that are applicable to all pieces. Subclasses should implement the
    `_calculate_legal_moves` and `get_attacked_squares` methods to define
    piece-specific movement and attack patterns.

    Attributes:
        color (PieceColor): The color of the chess piece, either BLACK or
        WHITE.

        position (Tuple[int, int]): The current position of the piece on the
        chessboard, represented as a tuple (row, column).

        value (PieceValue): The value of the piece based on its type, used in
        evaluating the board.

        name (PieceName): The name of the piece (e.g., PAWN, ROOK, etc.).

        board (Board): A reference to the chessboard the piece is on.

        move_story (List[Tuple[int, Tuple[int, int]]]): A history of the
        piece's moves, stored as a list of tuples containing the move number
        and the new position.

        first_move (bool): A flag indicating if the piece has moved yet.
        Important for pawns and castling rights.

        captured_by (Piece | None): A reference to the piece that captured
        this piece, if any.

    Properties:
        is_captured (bool): Returns True if the piece has been captured,
        False otherwise.

        algebraic_pos (str): The position of the piece in algebraic notation
        (e.g., "e4").

        row (int): The row component of the piece's position.

        column (int): The column component of the piece's position.

        sing_char (str): A single-character string representing the piece,
        derived from its name.

    Methods:

        capture(captured_by: 'Piece'): Marks this piece as captured by another
        piece.

        move_to(
            new_position: Union[Tuple[int, int], str],
            in_castleling: bool = False
        ):
        Moves the piece to a new position on the board, given in either
        coordinate tuple or algebraic notation.

        add_move_to_story(
            move_number: int,
            new_position: Union[Tuple[int, int], str]
        ):
        Records a move in the piece's move history.

        undo_move(): Reverts the piece's position to its previous state before
        the last move.

        scan_column(
            traspass_king: bool = False,
            get_only_squares: bool = False,
            end_at_piece_found: bool = True
        ):
        Scans the column for pieces or squares.

        scan_row(
            traspass_king: bool = False,
            get_only_squares: bool = False,
            end_at_piece_found: bool = True
        ):
        Scans the row for pieces or squares.

        scan_diagonals(
            end_at_piece_found: bool = True,
            traspass_king: bool = False,
            get_only_squares: bool = False
        ):
        Scans the diagonals for pieces or squares.

        calculate_legal_moves(
            show_in_algebraic_notation: bool = False,
            check_capturable_moves: bool = True,
            traspass_king: bool = False,
            get_only_squares: bool = False
        ):
        Calculates and returns all legal moves for the piece.

    Abstract Methods:
        _calculate_legal_moves(
            show_in_algebraic_notation: bool = False,
            check_capturable_moves: bool = True,
            traspass_king: bool = False,
            get_only_squares: bool = False
        ):
            To be implemented by subclasses to define specific legal moves.

        get_attacked_squares(
            show_in_algebraic_notation: bool = False
        ): To be implemented by subclasses to define the squares that
        the piece is attacking.
    """

    def __init__(
        self,
        color: PieceColor,
        position: tuple[int, int],
        value: PieceValue,
        name: PieceName,
        board: 'Board'
    ):
        """
        Initialize a new instance of a chess piece.

        Parameters:
            color (PieceColor): The color of the piece, either
            PieceColor.BLACK or PieceColor.WHITE.

            position (Tuple[int, int]): The starting position of the piece on
            the chessboard, represented as a tuple (row, column), where row
            and column are integers between 0 and 7.

            value (PieceValue): The relative value of the piece based on
            standard chess piece values.

            name (PieceName): The type of the chess piece
            (e.g., PieceName.PAWN, PieceName.ROOK).

            board ('Board'): A reference to the board object that the piece is
            placed on.

        Attributes initialized:

            move_story (List[Tuple[int, Tuple[int, int]]]): Initializes as an
            empty list to record the piece's move history.

            first_move (bool): Initialized to True, indicating that the piece
            has not moved yet.

            captured_by (Piece | None): Initialized to None, indicating the
            piece has not been captured.
        """

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

    def capture(self, captured_by: 'Piece'):
        self.captured_by = captured_by

    def move_to(
        self,
        new_position: tuple[int, int] | str,
        in_castleling: bool = False
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

        # check if is a pawn and check if the movement is en passant
        is_on_passant = False
        if self.name == PieceName.PAWN:
            if new_position == self._get_on_passant_square():
                is_on_passant = True

        if in_castleling or new_position in self.calculate_legal_moves():
            self.board.update_board(
                new_row=new_position[0],
                new_column=new_position[1],
                old_column=self.column,
                old_row=self.row,
                piece=self,
                is_en_passant=is_on_passant
            )

            self.position = new_position
            self.first_move = False

            return True

        return False

    def add_move_to_story(
        self,
        move_number: int,
        new_position: tuple[int, int] | str
    ):
        self.move_story.append((move_number, new_position))

    def undo_move(self):
        if self.move_story:
            move_number, last_position = self.move_story.pop()
            self.position = last_position
            if move_number == 1:
                self.first_move = True

    def scan_column(
        self,
        traspass_king: bool = False,
        get_only_squares: bool = False,
        end_at_piece_found: bool = True,
    ) -> dict:

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

        return self._scan_direction(
            for_value=self.row,
            board_scan_value=self.column,
            f_value_side=0,
            end_at_piece_found=end_at_piece_found,
            get_only_squares=get_only_squares,
            traspass_king=traspass_king
        )

    def scan_row(
        self,
        traspass_king: bool = False,
        get_only_squares: bool = False,
        end_at_piece_found: bool = True,
    ) -> dict:

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

        return self._scan_direction(
            for_value=self.column,
            board_scan_value=self.row,
            f_value_side=1,
            end_at_piece_found=end_at_piece_found,
            get_only_squares=get_only_squares,
            traspass_king=traspass_king
        )

    def scan_diagonals(
        self,
        end_at_piece_found: bool = True,
        traspass_king: bool = False,
        get_only_squares: bool = False
    ) -> dict:

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

        direction_0: list[Piece | None] = self._check_row_and_columns(
            start_range=range(self.row - 1, -1, -1),
            end_range=range(self.column - 1, -1, -1),
            end_at_piece_found=end_at_piece_found,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares
        )
        direction_1: list[Piece | None] = self._check_row_and_columns(
            start_range=range(self.row - 1, -1, -1),
            end_range=range(self.column + 1, 8),
            end_at_piece_found=end_at_piece_found,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares
        )
        direction_2: list[Piece | None] = self._check_row_and_columns(
            start_range=range(self.row + 1, 8),
            end_range=range(self.column - 1, -1, -1),
            end_at_piece_found=end_at_piece_found,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares
        )
        direction_3: list[Piece | None] = self._check_row_and_columns(
            start_range=range(self.row + 1, 8),
            end_range=range(self.column + 1, 8),
            end_at_piece_found=end_at_piece_found,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares
        )

        return {
            'd0': direction_0,
            'd1': direction_1,
            'd2': direction_2,
            'd3': direction_3
        }

    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        check_capturable_moves: bool = True,
        traspass_king: bool = False,
        get_only_squares: bool = False
    ) -> list[str | list[int, int]]:

        """
        Returns a list of legal moves for the piece.

        Parameters:
            show_in_algebraic_notation (bool): If True, returns the list of
            moves in algebraic notation. Defaults to False.
        """

        piece_legal_moves = self._calculate_legal_moves(
            traspass_king=traspass_king,
            get_only_squares=get_only_squares,
            check_capturable_moves=check_capturable_moves,
            show_in_algebraic_notation=show_in_algebraic_notation,
        )

        if self.name == PieceName.KING:
            return piece_legal_moves

        king_position = self._check_if_friendly_king_is_next_to_piece()

        if not king_position:
            return piece_legal_moves

        # check if the king is in a column, row, or diagonal within the piece

        moves = list()
        pieces_that_could_attack_king: list[PieceName] = list()

        is_row_or_column = False
        is_diagonal = False

        if king_position[0] == self.row:
            moves = self.scan_row()
            pieces_that_could_attack_king = [
                PieceName.ROOK,
                PieceName.QUEEN
            ]
            is_row_or_column = True

        elif king_position[1] == self.column:
            moves = self.scan_column()
            pieces_that_could_attack_king = [
                PieceName.ROOK,
                PieceName.QUEEN
            ]
            is_row_or_column = True

        else:
            # at this point, we know that the king is in a diagonal
            moves = self.scan_diagonals()
            pieces_that_could_attack_king = [
                PieceName.BISHOP,
                PieceName.QUEEN
            ]
            is_diagonal = True

            # d0 -> d4
            # d1 -> d2

        # check if there is a piece that could attack the king in the moves
        # list if the dictionary only have to keys, this mean that there is a
        # column or a row, so we need are sure that one of the directions have
        # a len of 1 and is the same color king, so descard that direction

        if is_row_or_column:
            directions = ['d0', 'd1']
            for index, dir in enumerate(directions):
                if len(moves[dir]) == 1:
                    p = moves[dir][0]
                    if isinstance(p, Piece):
                        if p.name == PieceName.KING and p.color == self.color:
                            moves = moves[directions[index - 1]]
                            break

        elif is_diagonal:

            # the complete diagonals are the following d0 -> d3
            # and d1 -> d2

            diagonals = [['d0', 'd3'], ['d1', 'd2']]
            terminate = False

            for diagonal in diagonals:
                for index, dir in enumerate(diagonal):
                    if len(moves[dir]) == 1:
                        p = moves[dir][0]
                        if isinstance(p, Piece):
                            if p.name == PieceName.KING and p.color == self.color:
                                moves = moves[diagonal[index - 1]]
                                terminate = True
                                break
                if terminate:
                    break

        if show_in_algebraic_notation:
            alg_moves = []
            for move in moves:
                if isinstance(move, Piece):
                    alg_moves.append(move)
                else:
                    alg_moves.append(convert_to_algebraic_notation(*move))

            moves = alg_moves

        if self._check_if_a_piece_can_attack_friendly_king_in_given_moves(
            moves=moves,
            pieces_to_check=pieces_that_could_attack_king
        ):
            # if there is a piece that could attack the king, we need to unify
            # the moves and the calculated legal moves, so the just the moves
            # that appear in both could be returned
            piece_legal_moves = list(set(piece_legal_moves) & set(moves))

        return piece_legal_moves

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

    @abstractmethod
    def _calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        check_capturable_moves: bool = True,
        traspass_king: bool = False,
        get_only_squares: bool = False
    ) -> list[str | list[int, int]]:

        """
        Returns a list of legal moves for the piece.

        Parameters:
            show_in_algebraic_notation (bool): If True, returns the list of
            moves in algebraic notation. Defaults to False.
        """
        pass

    def _check_if_friendly_king_is_next_to_piece(
        self,
    ) -> tuple[tuple[int, int]] | bool:
        """
        Check if the friendly king is next to the piece.
        """

        possible_king_positions = [
            (self.row - 1, self.column - 1),
            (self.row - 1, self.column),
            (self.row - 1, self.column + 1),
            (self.row, self.column - 1),
            (self.row, self.column + 1),
            (self.row + 1, self.column - 1),
            (self.row + 1, self.column),
            (self.row + 1, self.column + 1),
        ]

        for move in possible_king_positions:
            if self.board.is_position_on_board(move):
                piece = self.board.get_square_or_piece(*move)
                if isinstance(piece, Piece):
                    if piece.name == PieceName.KING:
                        if piece.color == self.color:
                            return piece.position
        return False

    def _scan_direction(
        self,
        for_value: int,
        board_scan_value: int,
        f_value_side: int,
        end_at_piece_found: bool = True,
        get_only_squares: bool = False,
        traspass_king: bool = False
    ):
        direction_0: list[Piece | None] = []
        direction_1: list[Piece | None] = []

        row_column = [None, None]

        # check the column in one direction
        for f_value in range(for_value - 1, -1, -1):

            row_column[f_value_side] = f_value
            row_column[1 - f_value_side] = board_scan_value

            direction_0.append(
                self.board.get_square_or_piece(*row_column)
            )
            if isinstance(direction_0[-1], Piece):
                if get_only_squares:
                    direction_0[-1] = direction_0[-1].position

                if end_at_piece_found:
                    break

        # check the column in another direction
        for f_value in range(for_value + 1, 8):

            row_column[f_value_side] = f_value
            row_column[1 - f_value_side] = board_scan_value

            direction_1.append(
                self.board.get_square_or_piece(*row_column)
            )
            last_square = direction_1[-1]

            if isinstance(last_square, Piece):
                if get_only_squares:
                    direction_1[-1] = last_square.position

                if last_square.name == PieceName.KING:
                    if traspass_king:
                        continue

                if end_at_piece_found:
                    break

        return {
            'd0': direction_0,
            'd1': direction_1
        }

    def _check_capturable_moves(
        self,
        moves: 'list[list[int, int], Piece | Piece]',
        check_only_last_move: bool = False
    ) -> list[tuple[int, int]]:

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

    def _check_row_and_columns(
        self,
        start_range: list[int],
        end_range: list[int],
        end_at_piece_found: bool = True,
        traspass_king: bool = False,
        get_only_squares: bool = False
    ) -> list[tuple[int, int]]:

        list_to_output: list[Piece | None] = []

        for row, column in zip(start_range, end_range):
            list_to_output.append(
                self.board.get_square_or_piece(row, column)
            )

            last_square = list_to_output[-1]

            if isinstance(list_to_output[-1], Piece):
                if get_only_squares:
                    list_to_output[-1] = last_square.position

                if last_square.name == PieceName.KING:
                    if traspass_king:
                        continue

                if end_at_piece_found:
                    break

        return list_to_output

    def _check_if_a_piece_can_attack_friendly_king_in_given_moves(
        self,
        moves: 'list[tuple[int, int] | Piece | str]',
        pieces_to_check: list[PieceName]
    ):

        for move in moves:
            if isinstance(move, Piece):
                if move.name in pieces_to_check and move.color != self.color:
                    return True

        return False

    def __str__(self):
        return f"{self.__class__.__name__}({self.color}, {self.algebraic_pos})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.color}, {self.algebraic_pos})"
