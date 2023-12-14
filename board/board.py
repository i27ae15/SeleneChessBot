from pieces import Piece, Pawn, Rook, Bishop, Knight, Queen, King
from pieces.utilites import PieceColor


class Board:

    """This class represents the board of the game."""

    def __init__(self) -> None:

        self.board: list[list[Piece | None]] = []
        self.create_initial_board_set_up()

    def __str__(self) -> str:
        self.print_board()
        return str()

    @staticmethod
    def is_position_on_board(
        self,
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
        self.board = self.create_empty_board()
        self.create_pawn_set_up()
        self.create_knight_set_up()
        self.create_bishop_set_up()
        self.create_rook_set_up()
        self.create_queen_set_up()
        self.create_king_set_up()

    def add_piece(
        self,
        piece: Piece | str,
        row: int | str | None = None,
        column: int | str | None = None,
        check_if_position_is_empty: bool = True
    ) -> bool:

        if piece:
            row = piece.row
            column = piece.column

        if isinstance(piece, Piece):
            if check_if_position_is_empty:
                if not self.is_position_empty(row=row, column=column):
                    return False
            self.board[row][column] = piece

        return True

    def create_pawn_set_up(self) -> list[list[Piece | None]]:
        for i in range(8):
            self.board[1][i] = Pawn(
                board=self,
                color=PieceColor.WHITE,
                position=(1, i)
            )
            self.board[6][i] = Pawn(
                board=self,
                color=PieceColor.BLACK,
                position=(6, i)
            )

    def create_knight_set_up(self) -> list[list[Piece | None]]:

        self.board[0][1] = Knight(PieceColor.WHITE, (0, 1), board=self)
        self.board[0][6] = Knight(PieceColor.WHITE, (0, 6), board=self)
        self.board[7][1] = Knight(PieceColor.BLACK, (7, 1), board=self)
        self.board[7][6] = Knight(PieceColor.BLACK, (7, 6), board=self)

    def create_bishop_set_up(self) -> list[list[Piece | None]]:
        self.board[0][2] = Bishop(PieceColor.WHITE, (0, 2), board=self)
        self.board[0][5] = Bishop(PieceColor.WHITE, (0, 5), board=self)
        self.board[7][2] = Bishop(PieceColor.BLACK, (7, 2), board=self)
        self.board[7][5] = Bishop(PieceColor.BLACK, (7, 5), board=self)

    def create_rook_set_up(self) -> list[list[Piece | None]]:
        self.board[0][0] = Rook(PieceColor.WHITE, (0, 0), board=self)
        self.board[0][7] = Rook(PieceColor.WHITE, (0, 7), board=self)
        self.board[7][0] = Rook(PieceColor.BLACK, (7, 0), board=self)
        self.board[7][7] = Rook(PieceColor.BLACK, (7, 7), board=self)

    def create_queen_set_up(self) -> list[list[Piece | None]]:
        self.board[0][3] = Queen(PieceColor.WHITE, (0, 3), board=self)
        self.board[7][3] = Queen(PieceColor.BLACK, (7, 3), board=self)

    def create_king_set_up(self) -> list[list[Piece | None]]:
        self.board[0][4] = King(PieceColor.WHITE, (0, 4), board=self)
        self.board[7][4] = King(PieceColor.BLACK, (7, 4), board=self)

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
