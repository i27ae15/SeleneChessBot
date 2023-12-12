from pieces import Piece, Pawn, Rook, Bishop, Knight, Queen, King
from pieces.utilites import PieceColor


class Board:

    """This class represents the board of the game."""

    def __init__(self) -> None:

        self.board: list[list[Piece | None]] = []
        self.create_initial_board_set_up()

    def __str__(self) -> str:
        self.print_board()
        return ''

    def is_position_empty(
        self,
        row: int | str,
        column: int | str
    ) -> bool:

        return self.board[row][column] is None

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
