from core.utils import convert_from_algebraic_notation, ALGEBRAIC_NOTATION

from pieces import Piece, Pawn, Rook, Bishop, Knight, Queen, King
from pieces.utilites import (
    PieceColor, PieceName, RookSide, NO_TRASPASS_KING_PIECES
)

from colorama import Fore, Style


class Board:

    """
    A class to represent a chess game board.

    This class manages the state and operations of a chess board,
    including piece placement, move legality, and board setup. It supports
    functionalities such as adding or removing pieces, checking if a position
    is empty or on the board, updating board state, and calculating legal moves
    and attacked squares. The board can be initialized with a default setup or
    left empty for custom piece placement.

    Attributes:

        board (list[list[Piece | None]]): A 2D list representing the board,
            where each element is either a Piece object or None.

        white_pieces (dict[list[Piece]]): A dictionary mapping PieceName to
            a list of white Piece objects on the board.

        black_pieces (dict[list[Piece]]): Similar to white_pieces, but for
            black pieces.

        pieces_on_board (dict[PieceColor, dict[list[Piece]]]): Maps each
            PieceColor to its respective pieces dictionary.

        castling_rights (dict[PieceColor, dict[RookSide, bool]]): Tracks
            the castling rights for each color and side.

        _attacked_squares (dict[PieceColor, list]): Internal tracking of
            squares attacked by each color.

        _attacked_squares_by_white_checked (bool): Flag to indicate if white's
            attacked squares have been checked.

        _attacked_squares_by_black_checked (bool): Similar flag for black.

        _is_initial_board_set_up (bool): Indicates if the initial board setup
            has been completed.

    Methods:
        __init__(create_initial_board_set_up=True): Initializes the board.

        is_position_on_board(position, row=None, column=None): Checks if a
            position is on the board.

        add_piece(piece, piece_color=None, row=None, column=None,
            algebraic_notation=None, check_if_position_is_empty=True,
            additional_information=None): Adds a piece to the board.

        create_empty_board(): Creates an empty board.

        clean_board(): Clears the board of all pieces.

        create_initial_board_set_up(): Sets up the board in the standard
            initial chess configuration.

        get_square_or_piece(row, column): Returns either the coordinates of
            an empty square or the occupying piece.

        get_legal_moves(color, show_in_algebraic_notation=False): Returns
            a list of legal moves for a given color.

        get_attacked_squares(color, show_in_algebraic_notation=False):
            Returns a list of squares attacked by a given color.

        get_piece(piece_name, color): Returns a list of pieces of a given
            name and color.

        is_position_empty(row, column): Checks if a given position is empty.

        remove_castling_rights(color): Removes castling rights for a given
            color.

        print_attacked_squares(perspective, piece_name=None): Prints the
            squares attacked by a given color or specific piece.

        print_board(perspective=PieceColor.WHITE, special_color_on=None,
            special_color=Fore.RED): Prints a representation of the
            board from a given perspective.

        update_board(old_row, old_column, new_row, new_column, piece,
            is_en_passant=False): Updates the board state after a move.

        get_board_representation(
            special_color_on=None,
            special_color=Fore.RED
        ):
            Generates a visual representation of the board with optional
            highlighting.

        _create_piece(
            piece_name,
            color,
            position,
            additional_information=None
        ):
            Creates a Piece object of the specified type and color at a given
            position.

        _create_initial_pawn_set_up(): Sets up the pawns on their initial
            positions on the board.

        _create_initial_knight_set_up(): Places the knights on their initial
            positions on the board.

        _create_initial_bishop_set_up(): Positions the bishops on their initial
            squares on the board.

        _create_initial_rook_set_up(): Arranges the rooks on their starting
            squares on the board.

        _create_initial_queen_set_up(): Places the queens on their initial
            positions on the board.

        _create_initial_king_set_up(): Sets the kings on their initial
            positions on the board.
    """

    def __init__(
        self,
        create_initial_board_set_up: bool = True,
        board_setup: list[list[str]] = None
    ) -> None:
        """
        Initialize a new Board instance.

        Initializes the chessboard, setting up various data structures to track
        pieces, castling rights, and attacked squares. Optionally sets up the
        board with the initial chess pieces arrangement.

        Parameters:
            create_initial_board_set_up (bool, optional): If True, the board
                is initialized with the standard chess setup. Default is True.

        Attributes:
            board (list[list[Piece | None]]): Represents the chessboard as a
                2D list where each element is a Piece or None.

            white_pieces, black_pieces (dict[list[Piece]]): Dictionaries
                holding lists of white and black Piece objects.

            pieces_on_board (dict[PieceColor, dict]): Maps each color to its
                respective pieces dictionary.

            castling_rights (dict[PieceColor, dict[RookSide, bool]]): Tracks
                castling rights for each color.

            _attacked_squares (dict[PieceColor, list]): Stores squares attacked
                by each color.

            _attacked_squares_by_white_checked,
            _attacked_squares_by_black_checked
                (bool): Flags indicating if attacked squares have been checked.

            _is_initial_board_set_up (bool): Indicates if initial board setup
                is done.
        """

        self.board: list[list[Piece | None]] = []
        self.white_pieces: dict[list[Piece]] = dict()
        self.black_pieces: dict[list[Piece]] = dict()

        self.pieces_on_board: dict[PieceColor] = {
            PieceColor.WHITE: self.white_pieces,
            PieceColor.BLACK: self.black_pieces
        }

        self.castleling_rights: dict[PieceColor] = {
            PieceColor.WHITE: {
                RookSide.KING: True,
                RookSide.QUEEN: True,
            },
            PieceColor.BLACK: {
                RookSide.KING: True,
                RookSide.QUEEN: True,
            }
        }

        self.n_white_pieces: int = 16
        self.n_black_pieces: int = 16

        self._attacked_squares: dict[PieceColor] = {
            PieceColor.WHITE: list(),
            PieceColor.BLACK: list()
        }
        self._attacked_squares_by_white_checked: bool = False
        self._attacked_squares_by_black_checked: bool = False

        self._is_initial_board_set_up: bool = False

        if create_initial_board_set_up:
            self.create_initial_board_set_up()

        if board_setup:
            self._setup_board(board_setup)

    @property
    def white_king(self) -> King:
        """
        Return the white king piece.

        Returns:
            King: The white king piece.
        """

        return self.get_piece(
            piece_name=PieceName.KING,
            color=PieceColor.WHITE
        )[0]

    @property
    def black_king(self) -> King:
        """
        Return the black king piece.

        Returns:
            King: The black king piece.
        """

        return self.get_piece(
            piece_name=PieceName.KING,
            color=PieceColor.BLACK
        )[0]

    @staticmethod
    def is_position_on_board(
        position: tuple[int, int],
        row: int | None = None,
        column: int | None = None
    ) -> bool:
        """
        Check if a specified position is on the chessboard.

        Determines whether a given position, either specified directly by row
        and column or by a tuple, is within the bounds of the chessboard.

        Parameters:
            position (tuple[int, int]): A tuple representing the (row, column)
                coordinates.
            row (int | None): Row index to check. Defaults to None.
            column (int | None): Column index to check. Defaults to None.

        Returns:
            bool: True if the position is on the board, False otherwise.
        """

        if position:
            row = position[0]
            column = position[1]

        if row is None or column is None:
            return False

        if row < 0 or row > 7:
            return False
        if column < 0 or column > 7:
            return False

        return True

    def decrement_piece_count(self, color: PieceColor):
        """
        Decrement the count of pieces for a given color.

        Parameters:
            color (PieceColor): The color for which to decrement the count.
        """

        if color == PieceColor.WHITE:
            self.n_white_pieces -= 1
        elif color == PieceColor.BLACK:
            self.n_black_pieces -= 1

    def add_piece(
        self,
        piece: Piece | PieceName,
        piece_color: PieceColor = None,
        row: int | str | None = None,
        column: int | str | None = None,
        algebraic_notation: str | None = None,
        check_if_position_is_empty: bool = True,
        additional_information: dict = None
    ) -> Piece:
        """
        Add a chess piece to the board at a specified position.

        This method adds a piece to the board, either at a specified row and
        column or using algebraic notation. It supports adding either a Piece
        object directly, or by specifying the type and color of the piece. If
        a king piece is being added, the method checks if a king of the same
        color is already present on the board and raises an error if so.
        The method also checks if the specified position is empty before
        adding the piece, unless overridden.

        Parameters:
            piece (Piece | PieceName): The chess piece to add, either as a
            Piece object or a PieceName.

            piece_color (PieceColor, optional): The color of the piece,
            required if piece is specified by name.

            row (int | str | None, optional): The row to place the piece, can
            be an integer or string.

            column (int | str | None, optional): The column to place the piece,
            can be an integer or string.

            algebraic_notation (str | None, optional): The position in
            algebraic notation, if specified, overrides row and column.

            check_if_position_is_empty (bool, optional): Whether to check if
            the position is empty before adding the piece (default is True).

        Returns:
            Piece: The piece that was added to the board.

        Raises:
            ValueError: If the specified position is not empty, or if piece
            color is not specified when required.
        """

        if self._is_initial_board_set_up:
            # check for the double kings
            is_king: bool = False
            king_color: PieceColor = None

            if isinstance(piece, PieceName):
                if piece == PieceName.KING:
                    is_king = True
                    king_color = piece_color
            elif isinstance(piece, Piece):
                if piece.name == PieceName.KING:
                    is_king = True
                    king_color = piece.color

            if is_king:
                if self.pieces_on_board[king_color].get(PieceName.KING):
                    raise ValueError(
                        f'The {king_color.name} king is already on the board.'
                    )

        if algebraic_notation:
            row, column = convert_from_algebraic_notation(algebraic_notation)

        if isinstance(piece, Piece):
            row = piece.row
            column = piece.column

        if check_if_position_is_empty:
            if not self.is_position_empty(row=row, column=column):
                raise ValueError(
                    'The position you are trying to add the piece to is '
                    'already occupied.'
                )

        if isinstance(piece, PieceName):
            if not piece_color:
                raise ValueError(
                    'You must specify the color of the piece to add.'
                )

            piece = self._create_piece(
                piece_name=piece,
                color=piece_color,
                position=(row, column),
                additional_information=additional_information
            )

        # add piece to the board
        self.board[row][column] = piece

        pieces_on_board = self.pieces_on_board[piece.color]

        if not pieces_on_board.get(piece.name):
            pieces_on_board[piece.name] = []

        # NOTE: could this be referencing to the piece.name instance of the
        # Sobject?
        pieces_on_board[piece.name].append(piece)

        return piece

    def create_empty_board(self):
        """
        Create an empty chessboard.

        Initializes the board as a 2D list with None values, representing an
        empty square on the chessboard.
        """

        self.board = [[None for _ in range(8)] for _ in range(8)]

    def clean_board(self):
        """
        Clear the chessboard of all pieces.

        Resets the board to an empty state and clears the dictionaries tracking
        the pieces for both white and black.
        """

        self.white_pieces = dict()
        self.black_pieces = dict()

        self.pieces_on_board = {
            PieceColor.WHITE: dict(),
            PieceColor.BLACK: dict()
        }
        self.create_empty_board()

    def create_initial_board_set_up(self) -> list[list[Piece | None]]:
        """
        Set up the initial arrangement of chess pieces on the board.

        Arranges the chess pieces in their standard starting positions. This
        includes setting up pawns, knights, bishops, rooks, queens, and kings
        for both white and black.

        Returns:
            list[list[Piece | None]]: The chessboard with the initial setup.

        Raises:
            ValueError: If the initial setup has already been created.
        """

        if self._is_initial_board_set_up:
            raise ValueError(
                'The initial board set up has already been created.'
            )

        self.create_empty_board()

        self._create_initial_pawn_set_up()
        self._create_initial_knight_set_up()
        self._create_initial_bishop_set_up()
        self._create_initial_rook_set_up()
        self._create_initial_queen_set_up()
        self._create_initial_king_set_up()

        self._is_initial_board_set_up = True

    def get_square_or_piece(
        self,
        row: int,
        column: int
    ) -> 'tuple[int, int] | Piece':

        """
        Determine if a square on the chessboard is empty or occupied by a
        piece.

        This method checks the specified square on the board. If the
        square is empty, it returns its coordinates. If the square is
        occupied by a chess piece, it returns the piece object.

        Parameters:
            row (int): The row index of the square to check.
            column (int): The column index of the square to check.

        Returns:
            list[int, int] | Piece: The coordinates of the square as a list
            if it's empty, the Piece object if it's occupied, or None if the
            square is not on the board.
        """

        move_or_piece: tuple[int, int] | Piece | None = []
        if self.board[row][column] is None:
            move_or_piece = (row, column)
        else:
            move_or_piece = self.board[row][column]

        return move_or_piece

    def get_legal_moves(
        self,
        color: PieceColor,
        show_in_algebraic_notation: bool = False,
    ) -> list[tuple[int, int]]:

        """
        Calculate and return all legal moves for a given color.

        Iterates through all pieces of the specified color and aggregates their
        legal moves. Optionally, the moves can be presented in algebraic
        notation.

        Parameters:
            color (PieceColor): The color of the pieces to calculate moves for.
            show_in_algebraic_notation (bool, optional): Whether to return
                moves in algebraic notation. Default is False.

        Returns:
            list[tuple[int, int]]: A list of tuples representing legal moves.
        """

        pieces = self.pieces_on_board[color]

        legal_moves = dict()

        for piece_key in pieces:
            for piece in pieces[piece_key]:
                piece: Piece
                # name = f'{piece.name.value[1]}_{piece.algebraic_pos}'
                legal_moves[piece] = piece.calculate_legal_moves(
                    show_in_algebraic_notation=show_in_algebraic_notation
                )

        return legal_moves

    def get_attacked_squares(
        self,
        color: PieceColor,
        traspass_king: bool = False,
        show_in_algebraic_notation: bool = False
    ) -> list[tuple[int, int]]:
        """
        Determine squares attacked by a given color.

        Computes and returns a list of squares that are under attack by the
        pieces of the specified color. Optionally, the squares can be
        represented in algebraic notation.

        Parameters:
            color (PieceColor): The color of the attacking pieces.
            show_in_algebraic_notation (bool, optional): Whether to return
                squares in algebraic notation. Default is False.

        Returns:
            list[tuple[int, int]]: A list of squares attacked by the specified
            color.
        """

        # TODO: we should update the variable self_attacked_squares to include
        # the moves where the attacked squares where calculated, and then
        # TODO: look a way to unify when show_in_algebraic_notation is True

        if color == PieceColor.WHITE:
            if self._attacked_squares_by_white_checked:
                return self._attacked_squares[PieceColor.WHITE]
            self._attacked_squares_by_white_checked = True

        elif color == PieceColor.BLACK:
            if self._attacked_squares_by_black_checked:
                return self._attacked_squares[PieceColor.BLACK]
            self._attacked_squares_by_black_checked = True

        attacked_squares = []

        piece_names = PieceName.__members__.values()

        for piece_name in piece_names:
            pieces = self.get_piece(
                piece_name=piece_name,
                color=color
            )

            for piece in pieces:
                extra_var = dict()
                if piece.name not in NO_TRASPASS_KING_PIECES:
                    extra_var['traspass_king'] = traspass_king
                    extra_var['king_color'] = color.opposite()

                piece: Piece
                attacked_squares += piece.get_attacked_squares(
                    show_in_algebraic_notation=show_in_algebraic_notation,
                    **extra_var
                )
        self._attacked_squares[color] = attacked_squares

        return attacked_squares

    def get_piece(
        self,
        piece_name: PieceName,
        color: PieceColor,
    ) -> list[Piece] | list:
        """
        Retrieve all pieces of a specified type and color.

        Parameters:
            piece_name (PieceName): The type of piece to retrieve.
            color (PieceColor): The color of the pieces to retrieve.

        Returns:
            list[Piece] | list: A list of pieces of the specified type and
            color.
        """
        return self.pieces_on_board[color][piece_name]

    def is_position_empty(
        self,
        row: int | str,
        column: int | str
    ) -> bool:
        """
        Check if a given board position is empty.

        Parameters:
            row (int | str): The row index or algebraic row to check.
            column (int | str): The column index or algebraic column to check.

        Returns:
            bool: True if the position is empty, False otherwise.
        """

        return self.board[row][column] is None

    def print_attacked_squares(
        self,
        traspass_king: bool = False,
        piece_name: PieceName | None = None,
        show_in_algebraic_notation: bool = True,
        perspective: PieceColor = PieceColor.WHITE,
    ):
        """
        Print the squares attacked from a specified perspective.

        Displays the squares currently under attack from the perspective of a
        specified color or specific piece.

        Parameters:
            perspective (PieceColor, optional): The color perspective to use.
                Default is PieceColor.WHITE.
            piece_name (PieceName | None, optional): Specific piece type to
                focus on. Default is None.
        """

        attacked_squares = list()

        # there is somethign wrong is we call the function like this
        if not piece_name:
            attacked_squares = self.get_attacked_squares(
                color=perspective,
                traspass_king=traspass_king,
            )

        else:
            pieces = self.get_piece(
                piece_name=piece_name,
                color=perspective
            )

            for piece in pieces:
                extra_var = dict()
                if piece.name not in NO_TRASPASS_KING_PIECES:
                    extra_var['traspass_king'] = traspass_king

                piece: Piece
                attacked_squares += piece.get_attacked_squares(**extra_var)

        self.print_board(
            perspective=perspective,
            special_color_on=attacked_squares,
            show_in_algebraic_notation=show_in_algebraic_notation
        )

    def remove_castleling_rights(self, color: PieceColor):
        """
        Remove castling rights for a given color.

        Parameters:
            color (PieceColor): The color for which to remove castling rights.
        """
        self.castleling_rights[color][RookSide.KING] = False
        self.castleling_rights[color][RookSide.QUEEN] = False

    def remove_piece(self, piece: Piece):
        """
        Remove a piece from the board.

        This method removes a piece from the board, updating the internal
        representation and the tracking dictionaries. It also removes the
        piece from the list of attacked squares for its color.

        Parameters:
            piece (Piece): The piece to remove.
        """

        self.board[piece.row][piece.column] = None
        self.pieces_on_board[piece.color][piece.name].remove(piece)

    def print_board(
        self,
        special_color: str = Fore.RED,
        show_in_algebraic_notation: bool = False,
        perspective: PieceColor = PieceColor.WHITE,
        special_color_on: tuple[tuple[int, int]] | None = None,
    ):
        """
        Print the chessboard from a specified perspective.

        This method displays the current state of the chessboard, optionally
        highlighting specific squares in a different color. The board can be
        viewed from either the white or black perspective.

        Parameters:
            perspective (PieceColor): The perspective from which to view
                the board. Defaults to PieceColor.WHITE.
            special_color_on (tuple[tuple[int, int]] | None): Tuples of
                coordinates to highlight on the board. Defaults to None.
            special_color (str): The color code (ANSI escape code) used for
                highlighting. Defaults to Fore.RED.

        Note:
            The board is printed to the console, with each square represented
            by either a '.' or the single-character representation of the
            piece occupying it.
        """

        board_representation = self.get_board_representation(
            special_color=special_color,
            special_color_on=special_color_on,
            show_in_algebraic_notation=show_in_algebraic_notation
        )

        if perspective == PieceColor.WHITE:
            board_representation.reverse()

        for row in board_representation:
            print(' '.join(row))

    def update_board(
        self,
        old_row: int,
        old_column: int,
        new_row: int,
        new_column: int,
        piece: Piece,
        is_en_passant: bool = False
    ):
        """
        Update the board state after a piece is moved.

        This method moves a piece from its old position to a new position on
        the board. It handles the removal of a pawn captured via en passant,
        if applicable.

        Parameters:
            old_row (int): The row index of the piece's current position.
            old_column (int): The column index of the piece's current position.
            new_row (int): The row index of the piece's new position.
            new_column (int): The column index of the piece's new position.
            piece (Piece): The piece object that is being moved.
            is_en_passant (bool, optional): Flag indicating whether the move
                is an en passant capture. Defaults to False.

        Note:
            This method updates the internal board representation and does not
            check the legality of the move.
        """

        self._manage_capture(
            row=new_row,
            column=new_column,
            is_en_passant=is_en_passant,
            piece_color=piece.color
        )

        self.board[old_row][old_column] = None
        self.board[new_row][new_column] = piece

    def get_board_representation(
        self,
        reverse: bool = False,
        use_colors: bool = True,
        special_color: str = Fore.RED,
        upper_case_diff: bool = False,
        show_in_algebraic_notation: bool = False,
        special_color_on: tuple[tuple[int, int]] | None = None,
    ) -> list[list[str]]:
        """
        Generate a string representation of the chessboard.

        This method creates a list of strings representing each square on the
        chessboard. Each square is represented by either a '.' for an empty
        square or the single-character representation of the piece occupying
        it. The method allows for highlighting specific squares in a special
        color.

        Parameters:
            special_color_on (tuple[tuple[int, int]] | None): A tuple of
                coordinate tuples (row, column) for squares to be highlighted.
                Default is None, indicating no highlighting.

            special_color (str): The color code (ANSI escape code) to use for
                highlighting. Default is Fore.RED.

            use_colors (bool): Whether to use ANSI color codes for the output.

            upper_case_diff (bool): Whether to use uppercase for white pieces
            and lowercase for black pieces.

        Returns:
            list[list[str]]: A 2D list representing the board, where each
            element is a string representing a square.
        """

        get_board_representation: list[list[str]] = []

        board = self.board

        if reverse:
            board = self.board.copy()
            board.reverse()

        for row_index, row in enumerate(board):
            current_row: list[str] = []
            for column_index, p in enumerate(row):

                char = str()
                color = Fore.WHITE

                algebraic_char = str()
                if show_in_algebraic_notation:
                    algebraic_char = (
                        ALGEBRAIC_NOTATION['column'][column_index] +
                        ALGEBRAIC_NOTATION['row'][row_index]
                    )

                if p is None:
                    if show_in_algebraic_notation:
                        char = algebraic_char
                    else:
                        char = '.'
                else:
                    char = p.sing_char

                    if show_in_algebraic_notation:
                        char += f'{algebraic_char[-1]}'

                    if p.color == PieceColor.BLACK:
                        if use_colors:
                            color = Fore.LIGHTBLUE_EX
                        if upper_case_diff:
                            char = char.lower()

                    if use_colors:
                        if p.color == PieceColor.WHITE:
                            color = Fore.LIGHTCYAN_EX

                if use_colors and special_color_on:
                    if (row_index, column_index) in special_color_on:
                        color = special_color
                if use_colors:
                    str_rep = f'{color}{char}{Style.RESET_ALL}'
                else:
                    str_rep = char
                current_row.append(str_rep)

            get_board_representation.append(current_row)

        return get_board_representation

    def _setup_board(self, board_setup: list[list[str]]):

        """

        A board setupt that should looks like this

        'board': [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

        Where the minuscule letters are black pieces and the capital letters
        are white pieces
        """

        if self._is_initial_board_set_up:
            raise ValueError(
                'The initial board set up has already been created.'
            )

        self.create_empty_board()
        for row_index, row in enumerate(board_setup):
            for column_index, piece in enumerate(row):
                if piece != '.':
                    piece_color = (
                        PieceColor.WHITE if piece.isupper()
                        else PieceColor.BLACK
                    )
                    piece = piece.upper()
                    self.add_piece(
                        piece=PieceName.get_piece_from_string(piece),
                        piece_color=piece_color,
                        row=row_index,
                        column=column_index
                    )

        self._is_initial_board_set_up = True

    def _create_piece(
        self,
        piece_name: PieceName,
        color: PieceColor,
        position: tuple[int, int],
        additional_information: dict = None
    ) -> Piece:
        """
        Create a Piece object based on specified parameters.

        This method instantiates a new piece object of the type specified by
        piece_name. The piece is created with the specified color and position
        on the board. Additional information can be passed to customize the
        piece's creation further.

        Parameters:
            piece_name (PieceName): The type of piece to create
            (e.g., PAWN, ROOK).

            color (PieceColor): The color of the piece (WHITE or BLACK).

            position (tuple[int, int]): The position (row, column) to place
            the piece.

            additional_information (dict, optional): Additional data to pass to
                the piece constructor. Defaults to an empty dictionary.

        Returns:
            Piece: The created Piece object.
        """

        if additional_information is None:
            additional_information = dict()

        piece_clases = {
            PieceName.PAWN: Pawn,
            PieceName.ROOK: Rook,
            PieceName.KNIGHT: Knight,
            PieceName.BISHOP: Bishop,
            PieceName.QUEEN: Queen,
            PieceName.KING: King
        }

        return piece_clases[piece_name](
            color=color,
            board=self,
            position=position,
            **additional_information
        )

    def _create_initial_pawn_set_up(self):
        """
        Set up the pawns on their initial positions on the chessboard.

        This method places all the pawns for both white and black on their
        respective starting rows (second row for white, seventh row for black).
        It updates the white_pieces and black_pieces dictionaries accordingly.
        """

        for i in range(8):

            self.add_piece(
                piece=PieceName.PAWN,
                piece_color=PieceColor.WHITE,
                row=1,
                column=i
            )
            self.add_piece(
                piece=PieceName.PAWN,
                piece_color=PieceColor.BLACK,
                row=6,
                column=i
            )

    def _create_initial_knight_set_up(self):
        """
        Place the knights on their initial positions on the chessboard.

        This method positions the knights for both white and black. Each color
        gets two knights, placed on their standard starting squares (b1, g1 for
        white and b8, g8 for black). The white_pieces and black_pieces
        dictionaries are updated with these knights.
        """

        self.add_piece(
            piece=PieceName.KNIGHT,
            piece_color=PieceColor.WHITE,
            row=0,
            column=1
        )

        self.add_piece(
            piece=PieceName.KNIGHT,
            piece_color=PieceColor.WHITE,
            row=0,
            column=6
        )
        self.add_piece(
            piece=PieceName.KNIGHT,
            piece_color=PieceColor.BLACK,
            row=7,
            column=1
        )
        self.add_piece(
            piece=PieceName.KNIGHT,
            piece_color=PieceColor.BLACK,
            row=7,
            column=6
        )

    def _create_initial_bishop_set_up(self):
        """
        Position the bishops on their initial squares on the chessboard.

        This method sets up the bishops for both white and black. Each color
        has two bishops, placed on their designated starting squares (c1, f1
        for white and c8, f8 for black). The white_pieces and black_pieces
        dictionaries are updated with these bishops.
        """

        self.add_piece(
            piece=PieceName.BISHOP,
            piece_color=PieceColor.WHITE,
            row=0,
            column=2
        )
        self.add_piece(
            piece=PieceName.BISHOP,
            piece_color=PieceColor.WHITE,
            row=0,
            column=5
        )

        self.add_piece(
            piece=PieceName.BISHOP,
            piece_color=PieceColor.BLACK,
            row=7,
            column=2
        )
        self.add_piece(
            piece=PieceName.BISHOP,
            piece_color=PieceColor.BLACK,
            row=7,
            column=5
        )

    def _create_initial_rook_set_up(self):
        """
        Arrange the rooks on their starting squares on the chessboard.

        This method places the rooks for both white and black on their
        respective corners of the board. Each color has two rooks, placed on
        a1, h1 for white and a8, h8 for black. The white_pieces and
        black_pieces dictionaries are updated accordingly. Additional
        information specifying the rook's side (QUEEN or KING) is also
        recorded.
        """

        self.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.WHITE,
            row=0,
            column=0,
            additional_information={'rook_side': RookSide.QUEEN}
        )
        self.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.WHITE,
            row=0,
            column=7,
            additional_information={'rook_side': RookSide.KING}
        )

        self.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.BLACK,
            row=7,
            column=0,
            additional_information={'rook_side': RookSide.QUEEN}
        )
        self.add_piece(
            piece=PieceName.ROOK,
            piece_color=PieceColor.BLACK,
            row=7,
            column=7,
            additional_information={'rook_side': RookSide.KING}
        )

    def _create_initial_queen_set_up(self):
        """
        Place the queens on their initial positions on the chessboard.

        This method sets up the queens for both white and black on their
        standard starting squares (d1 for white and d8 for black). The
        white_pieces and black_pieces dictionaries are updated with these
        queens.
        """

        self.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.WHITE,
            row=0,
            column=3
        )

        self.add_piece(
            piece=PieceName.QUEEN,
            piece_color=PieceColor.BLACK,
            row=7,
            column=3
        )

    def _create_initial_king_set_up(self):
        """
        Set the kings on their initial positions on the chessboard.

        This method places the kings for both white and black on their
        designated starting squares (e1 for white and e8 for black). The
        white_pieces and black_pieces dictionaries are updated with these
        kings.
        """

        self.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.WHITE,
            row=0,
            column=4
        )

        self.add_piece(
            piece=PieceName.KING,
            piece_color=PieceColor.BLACK,
            row=7,
            column=4
        )

    def _manage_capture(
        self,
        row: int,
        column: int,
        is_en_passant: bool,
        piece_color: PieceColor = None,
    ):

        if is_en_passant:
            # delete the pawn that was captured
            direction = -1 if piece_color == PieceColor.WHITE else 1
            piece = self.get_square_or_piece(
                row=row + direction,
                column=column,
            )
            self.board[row + direction][column] = None
        else:

            piece = self.get_square_or_piece(
                row=row,
                column=column,
            )
            if not isinstance(piece, Piece):
                return

            piece.capture(captured_by=piece)

        # delete the piece from the pieces_on_board dictionary
        self.decrement_piece_count(piece.color)
        self.pieces_on_board[piece.color][piece.name].remove(piece)

    def __str__(self) -> str:
        """
        Return a string representation of the board.

        This method overrides the default string representation of the Board
        object. It prints the current state of the chessboard, showing the
        positions of all pieces.

        Returns:
            str: The string representation of the board.
        """
        self.print_board()
        return str()
