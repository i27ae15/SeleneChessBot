from core.utilities import convert_from_algebraic_notation

from pieces import Piece, Pawn, Rook, Bishop, Knight, Queen, King
from pieces.utilites import PieceColor, PieceName


class Board:

    """This class represents the board of the game."""

    def __init__(self) -> None:

        self.board: list[list[Piece | None]] = []
        self.white_pieces: dict[list[Piece]] = dict()
        self.black_pieces: dict[list[Piece]] = dict()

        self.pieces_on_board: dict[PieceColor] = {
            PieceColor.WHITE: self.white_pieces,
            PieceColor.BLACK: self.black_pieces
        }

        self._is_initial_board_set_up = False

        self.create_initial_board_set_up()

    def __str__(self) -> str:
        self.print_board()
        return str()

    @staticmethod
    def is_position_on_board(
        position: tuple[int, int],
        row: int | None = None,
        column: int | None = None
    ) -> bool:

        """
        Check if a position is on the board.

        This method checks if the specified position is on the board.
        It can be called either with a tuple of coordinates or with
        separate row and column arguments.

        Parameters:
            position (tuple[int, int]): A tuple containing the coordinates
                of the position to check.
            row (int): The row index of the position to check.
            column (int): The column index of the position to check.

        Returns:
            bool: True if the position is on the board, False otherwise.
        """

        if position:
            row = position[0]
            column = position[1]

        if not row or not column:
            return False

        if row < 0 or row > 7:
            return False
        if column < 0 or column > 7:
            return False

        return True

    def is_position_empty(
        self,
        row: int | str,
        column: int | str
    ) -> bool:

        return self.board[row][column] is None

    def get_square_or_piece(
        self,
        row: int,
        column: int
    ) -> 'list[int, int] | Piece':

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

        move_or_piece: list[int, int] | Piece | None = []
        if self.board[row][column] is None:
            move_or_piece = [row, column]
        else:
            move_or_piece = self.board[row][column]

        return move_or_piece

    def create_empty_board(self) -> list[list[None]]:
        return [[None for _ in range(8)] for _ in range(8)]

    def create_initial_board_set_up(self) -> list[list[Piece | None]]:

        if self._is_initial_board_set_up:
            raise ValueError(
                'The initial board set up has already been created.'
            )

        self.board = self.create_empty_board()

        self._create_initial_pawn_set_up()
        self._create_initial_knight_set_up()
        self._create_initial_bishop_set_up()
        self._create_initial_rook_set_up()
        self._create_initial_queen_set_up()
        self._create_initial_king_set_up()

        self._is_initial_board_set_up = True

    def add_piece(
        self,
        piece: Piece | PieceName,
        piece_color: PieceColor = None,
        row: int | str | None = None,
        column: int | str | None = None,
        algebraic_notation: str | None = None,
        check_if_position_is_empty: bool = True
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
        piece (Piece | PieceName): The chess piece to add, either as a Piece
        object or a PieceName.

        piece_color (PieceColor, optional): The color of the piece, required
        if piece is specified by name.

        row (int | str | None, optional): The row to place the piece, can be
        an integer or string.

        column (int | str | None, optional): The column to place the piece,
        can be an integer or string.

        algebraic_notation (str | None, optional): The position in algebraic
        notation, if specified, overrides row and column.

        check_if_position_is_empty (bool, optional): Whether to check if the
        position is empty before adding the piece (default is True).

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
                if self.pieces_on_board[king_color][PieceName.KING]:
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
                position=(row, column)
            )

        self.board[row][column] = piece

        return piece

    def print_board(self, perspective: PieceColor = PieceColor.WHITE):

        board = self.board

        if perspective == PieceColor.WHITE:
            board = self.board.copy()
            board.reverse()

        for row in board:
            for p in row:
                if p is None:
                    print('.', end=' ')
                else:
                    print(f'{p.sing_char}', end=' ')
            print()

    def get_legal_moves(
        self,
        color: PieceColor,
        show_in_algebraic_notation: bool = False
    ) -> list[tuple[int, int]]:

        legal_moves = []

        for key in self.pieces_on_board[color]:
            pieces = self.pieces_on_board[color][key]
            for piece in pieces:
                piece: Piece
                legal_moves += piece.calculate_legal_moves(
                    show_in_algebraic_notation=show_in_algebraic_notation
                )

        return legal_moves

    def get_attacked_squares(
        self,
        color: PieceColor,
        show_in_algebraic_notation: bool = False
    ) -> list[tuple[int, int]]:

        # TODO: implement this method in each piece class

        attacked_squares = []

        for key in self.pieces_on_board[color]:
            pieces = self.pieces_on_board[color][key]
            for piece in pieces:
                piece: Piece
                attacked_squares += piece.get_attacked_squares(
                    show_in_algebraic_notation=show_in_algebraic_notation
                )

        return attacked_squares

    def get_piece(
        self,
        piece_name: PieceName,
        color: PieceColor,
    ) -> list[Piece] | list:
        return self.pieces_on_board[color][piece_name]

    def _create_piece(
        self,
        piece_name: PieceName,
        color: PieceColor,
        position: tuple[int, int]
    ) -> Piece:

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
            position=position
        )

    def _create_initial_pawn_set_up(self):
        white_pieces = []
        black_pieces = []
        for i in range(8):

            white_pieces.append(
                self.add_piece(
                    piece=PieceName.PAWN,
                    piece_color=PieceColor.WHITE,
                    row=1,
                    column=i
                )
            )

            black_pieces.append(
                self.add_piece(
                    piece=PieceName.PAWN,
                    piece_color=PieceColor.BLACK,
                    row=6,
                    column=i
                )
            )

        self.white_pieces[PieceName.PAWN] = white_pieces
        self.black_pieces[PieceName.PAWN] = black_pieces

    def _create_initial_knight_set_up(self):

        self.white_pieces[PieceName.KNIGHT] = []
        self.black_pieces[PieceName.KNIGHT] = []

        self.white_pieces[PieceName.KNIGHT].append(
            self.add_piece(
                piece=PieceName.KNIGHT,
                piece_color=PieceColor.WHITE,
                row=0,
                column=1
            )
        )
        self.white_pieces[PieceName.KNIGHT].append(
            self.add_piece(
                piece=PieceName.KNIGHT,
                piece_color=PieceColor.WHITE,
                row=0,
                column=6
            )
        )

        self.black_pieces[PieceName.KNIGHT].append(
            self.add_piece(
                piece=PieceName.KNIGHT,
                piece_color=PieceColor.BLACK,
                row=7,
                column=1
            )
        )
        self.black_pieces[PieceName.KNIGHT].append(
            self.add_piece(
                piece=PieceName.KNIGHT,
                piece_color=PieceColor.BLACK,
                row=7,
                column=6
            )
        )

    def _create_initial_bishop_set_up(self):

        self.white_pieces[PieceName.BISHOP] = []
        self.black_pieces[PieceName.BISHOP] = []

        self.white_pieces[PieceName.BISHOP].append(
            self.add_piece(
                piece=PieceName.BISHOP,
                piece_color=PieceColor.WHITE,
                row=0,
                column=2
            )
        )
        self.white_pieces[PieceName.BISHOP].append(
            self.add_piece(
                piece=PieceName.BISHOP,
                piece_color=PieceColor.WHITE,
                row=0,
                column=5
            )
        )

        self.black_pieces[PieceName.BISHOP].append(
            self.add_piece(
                piece=PieceName.BISHOP,
                piece_color=PieceColor.BLACK,
                row=7,
                column=2
            )
        )
        self.black_pieces[PieceName.BISHOP].append(
            self.add_piece(
                piece=PieceName.BISHOP,
                piece_color=PieceColor.BLACK,
                row=7,
                column=5
            )
        )

    def _create_initial_rook_set_up(self):

        self.white_pieces[PieceName.ROOK] = []
        self.black_pieces[PieceName.ROOK] = []

        self.white_pieces[PieceName.ROOK].append(
            self.add_piece(
                piece=PieceName.ROOK,
                piece_color=PieceColor.WHITE,
                row=0,
                column=0
            )
        )
        self.white_pieces[PieceName.ROOK].append(
            self.add_piece(
                piece=PieceName.ROOK,
                piece_color=PieceColor.WHITE,
                row=0,
                column=7
            )
        )

        self.black_pieces[PieceName.ROOK].append(
            self.add_piece(
                piece=PieceName.ROOK,
                piece_color=PieceColor.BLACK,
                row=7,
                column=0
            )
        )
        self.black_pieces[PieceName.ROOK].append(
            self.add_piece(
                piece=PieceName.ROOK,
                piece_color=PieceColor.BLACK,
                row=7,
                column=7
            )
        )

    def _create_initial_queen_set_up(self):

        self.white_pieces[PieceName.QUEEN] = []
        self.black_pieces[PieceName.QUEEN] = []

        self.white_pieces[PieceName.QUEEN].append(
            self.add_piece(
                piece=PieceName.QUEEN,
                piece_color=PieceColor.WHITE,
                row=0,
                column=3
            )
        )

        self.black_pieces[PieceName.QUEEN].append(
            self.add_piece(
                piece=PieceName.QUEEN,
                piece_color=PieceColor.BLACK,
                row=7,
                column=3
            )
        )

    def _create_initial_king_set_up(self):

        self.white_pieces[PieceName.KING] = []
        self.black_pieces[PieceName.KING] = []

        self.white_pieces[PieceName.KING].append(
            self.add_piece(
                piece=PieceName.KING,
                piece_color=PieceColor.WHITE,
                row=0,
                column=4
            )
        )

        self.black_pieces[PieceName.KING].append(
            self.add_piece(
                piece=PieceName.KING,
                piece_color=PieceColor.BLACK,
                row=7,
                column=4
            )
        )
