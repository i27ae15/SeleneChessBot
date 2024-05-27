from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable

from core.types import PositionT
from core.utils import (
    convert_from_algebraic_notation, convert_to_algebraic_notation
)

from .utilites import (
    PieceColor, PieceValue, PieceName, ATTACKING_ROWS_AND_COLUMNS,
    ATTACKING_DIAGONALS
)


if TYPE_CHECKING:
    from pieces import King
    from board import Board
    from game.piece_move import PieceMove


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
        position: PositionT,
        value: PieceValue,
        name: PieceName,
        board: 'Board',
        my_king: 'King' = None  # TODO: add the king when creating the piece
    ):
        """
        Initialize a new instance of a chess piece.

        Parameters:
            color (PieceColor): The color of the piece, either
            PieceColor.BLACK or PieceColor.WHITE.

            position (PositionT): The starting position of the piece on
            the chessboard, represented as a tuple (row, column), where row
            and column are integers between 0 and 7.

            value (PieceValue): The relative value of the piece based on
            standard chess piece values.

            name (PieceName): The type of the chess piece
            (e.g., PieceName.PAWN, PieceName.ROOK).

            board ('Board'): A reference to the board object that the piece is
            placed on.

        Attributes initialized:

            move_story (List[Tuple[int, PositionT]]): Initializes as an
            empty list to record the piece's move history.

            first_move (bool): Initialized to True, indicating that the piece
            has not moved yet.

            captured_by (Piece | None): Initialized to None, indicating the
            piece has not been captured.

            # TODO: Make possible to connect the board with the game,
            # so we can acces important information like the move number
        """

        self.color: PieceColor = color
        self.value: PieceValue = value

        self.first_move: bool = True
        self.name: PieceName = name
        self.board: 'Board' = board
        self.position: PositionT = position
        self.captured_by: Piece | None = None
        self.move_story: list[tuple[int, PositionT]] = []

        self.pieces_attacking_me: dict = dict()
        self.my_king: 'King' = my_king

    #  ---------------------------- PROPERTIES ----------------------------

    @property
    def get_my_king(self) -> 'King':
        if not self.my_king:
            self.my_king = self.board.get_piece(
                piece_name=PieceName.KING,
                color=self.color
            )[0]
        return self.my_king

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

    # ---------------------------- PUBLIC METHODS ----------------------------

    def add_move_to_story(
        self,
        move_number: int,
        new_position: tuple[int, int] | str
    ):
        self.move_story.append((move_number, new_position))

    def capture(self, captured_by: 'Piece'):
        self.captured_by = captured_by

    def move_to(
        self,
        new_position: PositionT | str,
        in_castleling: bool = False,
        piece_move: 'PieceMove' = None
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
        new_position (PositionT | str): The new position to move the
        piece to, either as a tuple of coordinates (row, column)
        or a string in algebraic notation.

        Returns:
        bool: True if the move is successful and legal, False otherwise.

        NOTE:
        - The method checks and updates castling rights if the piece is a rook
        or king moving for the first time. (this happens on the
        _validate_before_moving method on the subclasses of the piece class)

        - The legality of the move is determined by the `calculate_legal_moves`
        method of the piece.

        """

        self.__validate_before_moving()
        position_to, move_to_compare = self._get_position_to(
            new_position=new_position,
            piece_move=piece_move
        )

        is_on_passant = False
        if self.name == PieceName.PAWN:
            if position_to == self._get_on_passant_square():
                is_on_passant = True

        if in_castleling or move_to_compare in self.calculate_legal_moves():
            self.board.update_board(
                new_row=position_to[0],
                new_column=position_to[1],
                old_column=self.column,
                old_row=self.row,
                piece=self,
                is_en_passant=is_on_passant
            )

            self.position = tuple(position_to)
            self.first_move = False

            return True

        return False

    # ---------------------------- GETTER METHODS ----------------------------

    def get_pieces_under_attack(self) -> list['Piece']:
        """
        Returns a list of pieces that are under attack by the piece.
        """
        attacked_squares = self.get_attacked_squares()
        pieces_under_attack = []

        for square in attacked_squares:
            square = self.board.get_square_or_piece(*square)
            if isinstance(square, Piece):
                if square.color != self.color:
                    pieces_under_attack.append(square)
                    continue

        return pieces_under_attack

    def get_pieces_attacking_me(
        self,
        move_number: int = None
    ) -> list['Piece']:
        """
        Return a list of piece that are attacking this piece.

        If calculate_knights is True, the method will calculate the knights
        that are attacking the piece.
        """

        # if move_number:
        #     if self.pieces_attacking_me.get('calculated_at_moved') == move_number:
        #         return self.pieces_attacking_me['pieces']

        pieces_attacking_me: list[Piece] = []

        pieces_attacking_me += self.get_pieces_attacking_from_row_or_column()
        pieces_attacking_me += self.get_pieces_attacking_from_diagonals()
        pieces_attacking_me += self.get_knights_attacking_me()
        pieces_attacking_me += self.get_pawns_attacking_me()

        self.pieces_attacking_me = {
            'pieces': pieces_attacking_me,
            'calculated_at_moved': move_number
        }

        return pieces_attacking_me

    def get_pieces_attacking_from_row_or_column(self) -> list['Piece']:

        pieces_attacking_me: list[Piece] = []

        positions = ['d0', 'd1']

        columns = self.scan_column()
        rows = self.scan_row()

        for position in positions:
            # we only need to check the last position
            # and since both columns and rows have two directions
            # we can check both at the same time

            # for rows and columns we also need to check if the last element
            # is a rook or a queen
            if columns[position]:
                last_pos = columns[position][-1]
                if isinstance(last_pos, Piece):
                    if last_pos.color != self.color:
                        if last_pos.name in ATTACKING_ROWS_AND_COLUMNS:
                            pieces_attacking_me.append(last_pos)

            if rows[position]:
                last_pos = rows[position][-1]
                if isinstance(last_pos, Piece):
                    if last_pos.color != self.color:
                        if last_pos.name in ATTACKING_ROWS_AND_COLUMNS:
                            pieces_attacking_me.append(last_pos)

        return pieces_attacking_me

    def get_pieces_attacking_from_diagonals(self) -> list['Piece']:

        """
        NOTE:
            This does not check for pawns attacking the piece,
            call the get_pawns_attacking_me method for that
        """

        pieces_attacking_me: list[Piece] = []

        diagonals = self.scan_diagonals()
        positions = ['d0', 'd1', 'd2', 'd3']

        for position in positions:
            if diagonals[position]:
                last_pos = diagonals[position][-1]
                if isinstance(last_pos, Piece):
                    if last_pos.color != self.color:
                        if last_pos.name in ATTACKING_DIAGONALS:
                            pieces_attacking_me.append(diagonals[position][-1])

        return pieces_attacking_me

    def get_knights_attacking_me(self) -> list['Piece']:

        pieces_attacking_me: list[Piece] = []

        positions_to_check = [
            [self.row + 2, self.column + 1],
            [self.row + 2, self.column - 1],
            [self.row + 1, self.column + 2],
            [self.row + 1, self.column - 2],

            [self.row - 1, self.column + 2],
            [self.row - 1, self.column - 2],
            [self.row - 2, self.column + 1],
            [self.row - 2, self.column - 1],
        ]

        for pos in positions_to_check:

            piece = self._validate_piece_from_positions(
                position=pos,
                piece_name=PieceName.KNIGHT
            )
            if piece:
                pieces_attacking_me.append(piece)

        return pieces_attacking_me

    def get_pawns_attacking_me(self) -> list['Piece']:

        pieces_attacking_me: list[Piece] = []

        positions_to_check = [
            [self.row + 1, self.column + 1],
            [self.row + 1, self.column - 1],
            [self.row - 1, self.column + 1],
            [self.row - 1, self.column - 1],
        ]

        for pos in positions_to_check:
            piece = self._validate_piece_from_positions(
                position=pos,
                piece_name=PieceName.PAWN
            )
            if not piece:
                continue

            # get the attacking squares of the pawn
            attacking_squares = piece.get_attacked_squares()
            if self.position in attacking_squares:
                pieces_attacking_me.append(piece)

        return pieces_attacking_me

    # ---------------------------- SCANNER METHODS ----------------------------

    def scan_column(
        self,
        traspass_king: bool = False,
        king_color: PieceColor = None,
        get_only_squares: bool = False,
        end_at_piece_found: bool = True,
        get_in_algebraic_notation: bool = False
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
            f_value_side=0,
            for_value=self.row,
            king_color=king_color,
            traspass_king=traspass_king,
            board_scan_value=self.column,
            get_only_squares=get_only_squares,
            end_at_piece_found=end_at_piece_found,
            get_in_algebraic_notation=get_in_algebraic_notation
        )

    def scan_row(
        self,
        traspass_king: bool = False,
        king_color: PieceColor = None,
        get_only_squares: bool = False,
        end_at_piece_found: bool = True,
        get_in_algebraic_notation: bool = False
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
            f_value_side=1,
            for_value=self.column,
            king_color=king_color,
            board_scan_value=self.row,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares,
            end_at_piece_found=end_at_piece_found,
            get_in_algebraic_notation=get_in_algebraic_notation
        )

    def scan_diagonals(
        self,
        traspass_king: bool = False,
        king_color: PieceColor = None,
        get_only_squares: bool = False,
        end_at_piece_found: bool = True,
        get_in_algebraic_notation: bool = False
    ) -> dict:

        """
        Scan the diagonals where the piece is located until it finds another
        piece or the end of the board.

        This method scans all four diagonals from the current piece's position,
        collecting either the pieces or their positions into separate lists
        for each diagonal. The scanning stops based on various conditions,
        such as encountering a piece, finding a king of a specific color, or
        reaching the end of the board.

        Parameters:
        traspass_king (bool, optional): Whether to continue scanning if the
        piece is a king and matches the specified king color. Default is False.

        king_color (PieceColor, optional): The color of the king to check for
        when `traspass_king` is True. Default is None.

        get_only_squares (bool, optional): If True, collects only the
        positions of the squares instead of the pieces. Default is False.

        end_at_piece_found (bool, optional): If True, stops scanning upon
        finding a piece. Default is True.

        get_in_algebraic_notation (bool, optional): If True, returns positions
        in algebraic notation. Default is False.

        Returns:
            dict: A dictionary with four keys ('d0', 'd1', 'd2', 'd3'), each
            containing a list of pieces or positions found in the
            corresponding diagonal direction.

            the dictionary will have the following structure:

            {
                'd0': [PositionT | [Pieces]],
                'd1': [PositionT | [Pieces]],
                'd2': [PositionT | [Pieces]],
                'd3': [PositionT | [Pieces]]
            }

        """

        direction_0: list[Piece | None] = self._check_row_and_columns(
            start_range=range(self.row - 1, -1, -1),
            end_range=range(self.column - 1, -1, -1),
            end_at_piece_found=end_at_piece_found,
            traspass_king=traspass_king,
            king_color=king_color,
            get_only_squares=get_only_squares,
            get_in_algebraic_notation=get_in_algebraic_notation
        )

        direction_1: list[Piece | None] = self._check_row_and_columns(
            start_range=range(self.row - 1, -1, -1),
            end_range=range(self.column + 1, 8),
            end_at_piece_found=end_at_piece_found,
            traspass_king=traspass_king,
            king_color=king_color,
            get_only_squares=get_only_squares,
            get_in_algebraic_notation=get_in_algebraic_notation
        )
        direction_2: list[Piece | None] = self._check_row_and_columns(
            start_range=range(self.row + 1, 8),
            end_range=range(self.column - 1, -1, -1),
            end_at_piece_found=end_at_piece_found,
            traspass_king=traspass_king,
            king_color=king_color,
            get_only_squares=get_only_squares,
            get_in_algebraic_notation=get_in_algebraic_notation
        )
        direction_3: list[Piece | None] = self._check_row_and_columns(
            start_range=range(self.row + 1, 8),
            end_range=range(self.column + 1, 8),
            end_at_piece_found=end_at_piece_found,
            traspass_king=traspass_king,
            king_color=king_color,
            get_only_squares=get_only_squares,
            get_in_algebraic_notation=get_in_algebraic_notation
        )

        return {
            'd0': direction_0,
            'd1': direction_1,
            'd2': direction_2,
            'd3': direction_3
        }

    def scan_direction_for_piece_at_end(
        self,
        direction: int,
        piece_to_find: 'Piece',
        show_in_algebraic_notation: bool = False
    ) -> list[PositionT, str] | bool:

        """
        Scan the board in specified directions to find if a particular piece
        is at the end of any direction.

        This method scans the board in one or more specified directions to
        check if the specified piece is at the end of the scan.
        The directions are determined by the `direction` parameter, and the
        scan results can be returned in algebraic notation if specified.

        Parameters:
        direction (int): The direction(s) to scan:
                        0 -> column
                        1 -> row
                        2 -> diagonal
                        3 -> column & row
                        4 -> diagonal & row & column

        piece_to_find ('Piece'): The piece instance to find at the end of the
        scan.

        show_in_algebraic_notation (bool, optional): If True, returns
        positions in algebraic notation. Default is False.

        Returns:
            list[PositionT, str] | bool: The list of positions or pieces
            in the direction where the piece was found at the end, or False if
            not found.
        """

        # Dictionary mapping direction values to the corresponding scan methods
        directions_to_scan = {
            0: [self.scan_column],
            1: [self.scan_row],
            2: [self.scan_diagonals],
            3: [self.scan_column, self.scan_row],
            4: [self.scan_column, self.scan_row, self.scan_diagonals]
        }

        # Iterate over the selected scan methods based on the provided
        # direction
        for dir in directions_to_scan[direction]:
            # Call the scan method and get the results
            dirs: dict = dir(
                get_in_algebraic_notation=show_in_algebraic_notation
            )

            # Iterate over the results from the scan method
            for key in dirs:
                direction: list = dirs[key]

                # Skip empty directions
                if not direction:
                    continue

                # Check if the piece_to_find is at the end of the current
                # direction
                if piece_to_find == direction[-1]:
                    return direction

        # Return False if the piece was not found in any direction
        return False

    def calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        check_capturable_moves: bool = True,
        traspass_king: bool = False,
        king_color: PieceColor = None,
        get_only_squares: bool = False
    ) -> list[str | PositionT]:

        """
        Returns a list of legal moves for the piece.

        Parameters:
            show_in_algebraic_notation (bool): If True, returns the list of
            moves in algebraic notation. Defaults to False.

        """

        piece_legal_moves = self._calculate_legal_moves(
            king_color=king_color,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares,
            check_capturable_moves=check_capturable_moves,
            show_in_algebraic_notation=show_in_algebraic_notation,
        )

        if self.name == PieceName.KING:
            return piece_legal_moves

        # check if the king is under attack
        moves_dict, direction = self._detect_friendly_king_in_directions(
            get_in_algebraic_notation=show_in_algebraic_notation
        )

        if moves_dict:
            moves = moves_dict['d0'] + moves_dict['d1']
            piece_legal_moves = self._intersect_moves_with_king_helper(
                direction=direction,
                moves_to_scan=moves,
                piece_legal_moves=piece_legal_moves,
                get_in_algebraic_notation=show_in_algebraic_notation,
            )

        if self.get_my_king.check_if_in_check():
            return self._king_in_check_moves_helper(
                piece_legal_moves=piece_legal_moves,
                get_in_algebraic_notation=show_in_algebraic_notation
            )

        return piece_legal_moves

    # ---------------------------- PRIVATE METHODS ----------------------------

    def _validate_piece_from_positions(
        self,
        position: PositionT,
        piece_name: list[PieceName] | PieceName | None
    ) -> 'Piece | None':

        """
            Validate a piece at the given position on the board.

            Parameters
            ----------
            position : PositionT
                The position on the board to validate.

            piece_name : list[PieceName] | PieceName | None
                The name(s) of the piece to validate.
                Can be a single name, a list of names, or None.

            Returns
            -------

            Piece | None
                The piece if it is valid and matches the given criteria,
                otherwise None.

            Validates that the position is on the board and contains a piece
            that matches the given name(s) and is not of the same color as
            the player.
        """

        if not self.board.is_position_on_board(position):
            return

        piece = self.board.get_square_or_piece(*position)

        if not isinstance(piece, Piece):
            return

        if piece_name is not None:
            if not isinstance(piece_name, Iterable):
                piece_name = [piece_name]

            if piece.name not in piece_name:
                return

        if piece.color == self.color:
            return

        return piece

    def _detect_friendly_king_in_directions(
        self,
        get_in_algebraic_notation: bool = False
    ) -> tuple[PositionT, int] | bool:
        """
        Check if the friendly king is in the same diagonal, row, or column as
        the piece.

        This method scans the board in columns, rows, and diagonals to check
        if the friendly king is present. It returns the direction where the
        king is located and an integer representing the direction.

        The directions are represented as follows:
            0 -> column
            1 -> row
            2 -> diagonal

        Parameters:
            get_in_algebraic_notation (bool, optional): If True, returns
            positions in algebraic notation.

        Returns:
            tuple: A tuple containing the scan result and direction index if
            the king is found, otherwise (False, -1).
        """

        # Directions for columns and rows
        directions = ['d0', 'd1']
        # Directions for diagonals
        diagonals_dir = ['d0', 'd1', 'd2', 'd3']
        # List of scan methods for columns, rows, and diagonals
        scan_methods = [self.scan_column, self.scan_row, self.scan_diagonals]
        # Corresponding directions to check for each scan method
        directions_to_scan = [directions, directions, diagonals_dir]

        # Iterate over the scan methods and their corresponding directions
        for index, method in enumerate(scan_methods):
            # Perform the scan using the current method
            scan_result = method(
                get_in_algebraic_notation=get_in_algebraic_notation
            )
            current_directions = directions_to_scan[index]

            # Check each direction in the current scan result
            for direction in current_directions:
                moves = scan_result[direction]

                # Skip empty directions
                if not moves:
                    continue

                # Get the last square in the current direction
                last_square = moves[-1]
                # Check if the last square contains a friendly king
                if (
                    isinstance(last_square, Piece) and
                    last_square.name == PieceName.KING and
                    last_square.color == self.color
                ):
                    # Return the scan result and direction index for columns
                    # and rows
                    if index in [0, 1]:
                        return scan_result, index

                    # Prepare the return value for diagonals
                    to_return = {}
                    if direction in ['d0', 'd3']:
                        to_return = {
                            'd0': scan_result['d0'],
                            'd1': scan_result['d3']
                        }
                    elif direction in ['d1', 'd2']:
                        to_return = {
                            'd0': scan_result['d1'],
                            'd1': scan_result['d2']
                        }
                    return to_return, 2
        # Return False if no friendly king is found in any direction
        return False, -1

    def _scan_direction(
        self,
        for_value: int,
        f_value_side: int,
        board_scan_value: int,
        traspass_king: bool = False,
        king_color: PieceColor = None,
        get_only_squares: bool = False,
        end_at_piece_found: bool = True,
        get_in_algebraic_notation: bool = False
    ):

        """
        Scan the board in two directions from a given position and collect
        pieces or squares based on specified conditions.

        This method scans the board in two opposite directions from a starting
        position, collecting either pieces or their positions into two
        separate lists. The scanning is done on the _scanner_helper method.

        Parameters:

        for_value (int): The starting value for the direction scan.

        f_value_side (int): The index (0 or 1) to be varied during the scan.

        board_scan_value (int): The fixed value for the other index during the
        scan.

        traspass_king (bool, optional): Whether to continue scanning if the
        piece is a king and matches the specified king color. Default is False.

        king_color (PieceColor, optional): The color of the king to check for
        when `traspass_king` is True. Default is None.

        get_only_squares (bool, optional): If True, collects only the
        positions of the squares instead of the pieces. Default is False.

        end_at_piece_found (bool, optional): If True, stops scanning upon
        finding a piece. Default is True.

        get_in_algebraic_notation (bool, optional): If True, returns positions
        in algebraic notation. Default is False.

        Returns:
            dict: A dictionary with two keys, 'd0' and 'd1', each containing a
            list of pieces or positions found in the two scan directions.
        """

        direction_0 = self._scan_direction_helper(
            step=-1,
            end_value=-1,
            start_value=for_value - 1,
            f_value_side=f_value_side,
            board_scan_value=board_scan_value,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares,
            king_color=king_color,
            end_at_piece_found=end_at_piece_found,
            get_in_algebraic_notation=get_in_algebraic_notation
        )

        direction_1 = self._scan_direction_helper(
            step=1,
            end_value=8,
            start_value=for_value + 1,
            f_value_side=f_value_side,
            board_scan_value=board_scan_value,
            traspass_king=traspass_king,
            get_only_squares=get_only_squares,
            king_color=king_color,
            end_at_piece_found=end_at_piece_found,
            get_in_algebraic_notation=get_in_algebraic_notation
        )

        return {
            'd0': direction_0,
            'd1': direction_1
        }

    def _check_capturable_moves(
        self,
        moves: 'list[PositionT, Piece | Piece]',
        check_only_last_move: bool = False,
        get_in_algebraic_notation: bool = False
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
                    if get_in_algebraic_notation:
                        moves[-1] = moves[-1].algebraic_pos
                    else:
                        moves[-1] = tuple(moves[-1].position)
        else:
            for index, move in enumerate(moves):
                if isinstance(move, Piece):
                    is_capturable = True
                    if move.color == self.color:
                        is_capturable = False
                        moves.pop(index)

                    if is_capturable:
                        if get_in_algebraic_notation:
                            moves[index] = move.algebraic_pos
                        else:
                            moves[index] = tuple(move.position)
        return moves

    def _check_row_and_columns(
        self,
        start_range: list[int],
        end_range: list[int],
        end_at_piece_found: bool = True,
        traspass_king: bool = False,
        king_color: PieceColor = None,
        get_only_squares: bool = False,
        get_in_algebraic_notation: bool = False
    ) -> list[tuple[int, int]]:

        """
        Check and process a series of positions on the board defined by the
        given ranges for rows and columns.

        This method scans through positions on the board specified by the
        start and end ranges for rows and columns, collecting either pieces or
        their positions into a list. The scanning stops based on various
        conditions, such as encountering a piece, finding a king of a specific
        color, or reaching the end of the range.

        Parameters:

        start_range (list[int]): The starting range of values for the rows.

        end_range (list[int]): The ending range of values for the columns.

        end_at_piece_found (bool, optional): If True, stops scanning upon
        finding a piece. Default is True.

        traspass_king (bool, optional): Whether to continue scanning if the
        piece is a king and matches the specified king color. Default is False.

        king_color (PieceColor, optional): The color of the king to check for
        when `traspass_king` is True. Default is None.

        get_only_squares (bool, optional): If True, collects only the
        positions of the squares instead of the pieces. Default is False.

        get_in_algebraic_notation (bool, optional): If True, returns positions
        in algebraic notation. Default is False.

        Returns:
            list[tuple[int, int]]: A list of tuples representing either the
            pieces or their positions found during the scan.

        NOTE:
            This is not being done on the _scanner_helper method because
            the way the foor loops works is different from the other methods
            so to avoid over complicating the code, this is done here.

            Yes, we could just implement the part where it checks the squares
            into a separete method so we can call it there, but this will
            increase the runtime due to the over calling of the method which is
            not necessary.
        """

        list_to_output: list[Piece | None] = []

        for row, column in zip(start_range, end_range):
            list_to_output.append(
                self.board.get_square_or_piece(
                    row,
                    column,
                    get_in_algebraic_notation=get_in_algebraic_notation
                )
            )
            last_square = list_to_output[-1]

            if isinstance(last_square, Piece):
                if get_only_squares:
                    list_to_output[-1] = last_square.position

                if last_square.name == PieceName.KING:
                    if traspass_king and last_square.color == king_color:
                        continue

                if end_at_piece_found:
                    break

        return list_to_output

    # ---------------------------- HELPER METHODS ----------------------------

    def _intersect_moves_with_king_helper(
        self,
        direction: int,
        piece_legal_moves: list[PositionT],
        moves_to_scan: 'list[PositionT | Piece | str]',
        get_in_algebraic_notation: bool = False
    ) -> list:
        """
        Intersect the legal moves of the piece with potential attacking moves
        to protect the friendly king.

        This method checks if there are any pieces in the given moves that can
        attack the friendly king. If such pieces are found, it returns the
        intersection of the legal moves of the piece and the potential
        attacking moves.

        Parameters:

            direction (int): The direction to check for potential attacks
            (0 for column, 1 for row, 2 for diagonal).

            piece_legal_moves (list[PositionT]): The list of legal moves for
            the piece.

            moves_to_scan (list[PositionT | Piece | str]): The list of moves
            to scan for potential attackers.

            get_in_algebraic_notation (bool, optional): If True, converts the
            moves to algebraic notation. Default is False.

        Returns:
            list[PositionT]: The list of legal moves for the piece that also
            protect the king.
        """

        attacking_pieces: list[PieceName] = None

        if direction == 0 or direction == 1:
            attacking_pieces = ATTACKING_ROWS_AND_COLUMNS

        else:
            attacking_pieces = ATTACKING_DIAGONALS

            # d0 -> d4
            # d1 -> d2

        if self._check_if_a_piece_can_attack_friendly_king_in_given_moves(
            moves=moves_to_scan,
            pieces_to_check=attacking_pieces
        ):
            # if there is a piece that could attack the king, we need to
            # unify the moves and the calculated legal moves, so the just
            # the moves that appear in both could be returned
            # convert all moves to position
            for index, move in enumerate(moves_to_scan):
                if isinstance(move, Piece):
                    if get_in_algebraic_notation:
                        moves_to_scan[index] = move.algebraic_pos
                    else:
                        moves_to_scan[index] = move.position
            piece_legal_moves = list(
                set(piece_legal_moves) & set(moves_to_scan)
            )
        return piece_legal_moves

    def _king_in_check_moves_helper(
        self,
        piece_legal_moves: list[PositionT],
        get_in_algebraic_notation: bool = False
    ) -> list[PositionT]:
        """
        Helper method to calculate legal moves when the king is in check.

        This method determines if there is any move that the piece can make to
        block an enemy piece from attacking the friendly king. If the king is
        under double check, it returns an empty list, as the king must move.
        Otherwise, it returns the legal moves that block the check.

        Parameters:
            piece_legal_moves (list[PositionT]): The list of legal moves for
            the piece.
            get_in_algebraic_notation (bool, optional): If True, converts the
            moves to algebraic notation. Default is False.

        Returns:
            list[PositionT]: The list of possible legal moves that block the
            check.

            NOTE:
                This should be implemented in each Piece, on the
                _calculate_legal_moves, more complex, but more efficient.

                If this method is eliminated, it could increase the runtime
                in a 20% to 30%.
        """
        possible_legal_moves = []
        # Get the pieces attacking the friendly king
        pieces: list[Piece] = self.get_my_king.pieces_attacking_me['pieces']

        # If more than one piece is attacking, the king is in double check
        if len(pieces) > 1:
            return []

        # Dictionary mapping pieces to their respective scan directions
        directions_to_scan = {
            PieceName.BISHOP: 2,
            PieceName.ROOK: 3,
            PieceName.QUEEN: 4,
        }
        piece: Piece = pieces[0]

        # Determine the direction from which the piece is attacking the king
        direction = []
        if piece.name in directions_to_scan:
            direction = directions_to_scan[piece.name]
            direction = self.get_my_king.scan_direction_for_piece_at_end(
                direction=direction,
                piece_to_find=piece,
                show_in_algebraic_notation=get_in_algebraic_notation
            )

        # Check if any of the piece's legal moves can block the check
        for move in piece_legal_moves:
            if isinstance(move, Piece):
                if move == piece:
                    possible_legal_moves.append(move)
            else:
                if move in direction:
                    possible_legal_moves.append(move)
                if move == piece.position or move == piece.algebraic_pos:
                    possible_legal_moves.append(move)

        return possible_legal_moves

    def _scan_direction_helper(
        self,
        step: int,
        end_value: int,
        start_value: int,
        f_value_side: int,
        traspass_king: bool,
        board_scan_value: int,
        get_only_squares: bool,
        king_color: PieceColor,
        end_at_piece_found: bool,
        get_in_algebraic_notation: bool
    ) -> bool:
        """
        Process squares or pieces on the board in a specific direction and
        update the direction list based on specified conditions.

        This method iterates over board positions in a specified direction,
        appending each square or piece to the direction list. If a square
        contains a piece, it checks various conditions  such as encountering
        a piece, finding a king of a specific color,
        or reaching the end of the board.

        Parameters:
        step (int): The step value for the iteration, determining the
        direction of the scan.

        end_value (int): The end value for the iteration range.

        start_value (int): The starting value for the iteration range.

        f_value_side (int): The index (0 or 1) to be varied during the scan.

        traspass_king (bool): Whether to continue processing if the piece is a
        king and matches the specified king color.

        board_scan_value (int): The fixed value for the other index during the
        scan.

        get_only_squares (bool): If True, replaces pieces in the direction
        list with their positions.

        king_color (PieceColor): The color of the king to check for when
        `traspass_king` is True.

        end_at_piece_found (bool): If True, stops processing upon finding
        a piece.

        get_in_algebraic_notation (bool): If True, returns positions
        in algebraic notation.

        Returns:
        list: The list of squares or pieces found during the scan.
        """

        # Initialize the list to store the pieces or positions found in the
        # direction
        direction_list: list[Piece | None] = []

        # Initialize the row and column values
        row_column = [None, None]

        # Iterate over the range of values to scan in the specified direction
        for f_value in range(start_value, end_value, step):
            # Update the row or column value based on f_value_side
            row_column[f_value_side] = f_value
            row_column[1 - f_value_side] = board_scan_value

            # Append the square or piece found at the current position to the
            # direction list
            direction_list.append(
                self.board.get_square_or_piece(
                    *row_column,
                    get_in_algebraic_notation=get_in_algebraic_notation
                )
            )

            # Get the last square or piece added to the direction list
            last_square = direction_list[-1]

            # Check if the last square is a piece
            if isinstance(last_square, Piece):
                # If only square positions are needed, replace the piece with
                # its position
                if get_only_squares:
                    direction_list[-1] = last_square.position

                # If the piece is a king and matches the specified color,
                # determine if scanning should continue
                if last_square.name == PieceName.KING:
                    if traspass_king and last_square.color == king_color:
                        continue

                # If the scan should end upon finding a piece, break the loop
                if end_at_piece_found:
                    break

        # Return the list of squares or pieces found during the scan
        return direction_list

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

    def _get_position_to(
        self,
        new_position: PositionT | str,
        piece_move: 'PieceMove' = None,
    ) -> tuple[PositionT, PositionT | str]:

        position_to: PositionT | str = new_position
        move_to_compare: PositionT | str = new_position

        # Check if the position is a string
        if isinstance(new_position, str):
            # If the pieve_move does not have a coronation into, then, just
            # convert the string into the PositionT representation
            if not piece_move.coronation_into:
                alg_notation = convert_from_algebraic_notation(new_position)
                return alg_notation, alg_notation

            # If the piece_move object has a coronation into, then, we convert
            # the square where the piece is going to be coronated
            position_to = convert_from_algebraic_notation(
                position=piece_move.square
            )
            move_to_compare = piece_move.move_to_compare

        return position_to, move_to_compare

    # -------------------------- __PRIVATE METHODS ----------------------------

    def __validate_before_moving(self):

        """
        Optionally validates the move if
        a `_validate_before_moving` method is defined in the subclass.
        """

        if hasattr(self, '_validate_before_moving'):
            self._validate_before_moving()

    # ---------------------------- ABSTRACT METHODS ---------------------------

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
        raise NotImplementedError

    @abstractmethod
    def _calculate_legal_moves(
        self,
        show_in_algebraic_notation: bool = False,
        check_capturable_moves: bool = True,
        traspass_king: bool = False,
        king_color: PieceColor = None,
        get_only_squares: bool = False
    ) -> list[str | list[int, int]]:

        """
        Returns a list of legal moves for the piece.

        Parameters:
            show_in_algebraic_notation (bool): If True, returns the list of
            moves in algebraic notation. Defaults to False.
        """
        raise NotImplementedError

    # ---------------------------- DUNDER METHODS ---------------------------

    def __str__(self):
        return f"{self.__class__.__name__}({self.color}, {self.algebraic_pos})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.color}, {self.algebraic_pos})"
