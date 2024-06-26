from enum import Enum


class PieceColor(Enum):
    WHITE = 0
    BLACK = 1

    def opposite(self):
        if self == PieceColor.WHITE:
            return PieceColor.BLACK
        else:
            return PieceColor.WHITE

    @staticmethod
    def get_opposite(color):
        if color == PieceColor.WHITE:
            return PieceColor.BLACK
        else:
            return PieceColor.WHITE

    @staticmethod
    def choices():
        return [(piece.value, piece.name) for piece in PieceColor]


class PieceValue(Enum):
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
    KING = float('inf')


class PieceName(Enum):
    PAWN = 'Pawn', 'P'
    BISHOP = 'Bishop', 'B'
    KNIGHT = 'Knight', 'N'
    ROOK = 'Rook', 'R'
    QUEEN = 'Queen', 'Q'
    KING = 'King', 'K'

    @staticmethod
    def get_piece_from_string(piece_string) -> 'PieceName':
        for piece in PieceName:
            if piece_string in piece.value:
                return piece
        raise ValueError(f"Invalid piece string: {piece_string}")


class RookSide(Enum):
    QUEEN = 0
    KING = 1


NO_TRASPASS_KING_PIECES = [
    PieceName.PAWN,
    PieceName.KING,
    PieceName.KNIGHT
]

ATTACKING_ROWS_AND_COLUMNS = [
    PieceName.ROOK,
    PieceName.QUEEN,
]

ATTACKING_DIAGONALS = [
    PieceName.BISHOP,
    PieceName.QUEEN,
]

STARTING_POSITIONS_FOR_W_PAWNS = [
    (1, 0), (1, 1), (1, 2), (1, 3),
    (1, 4), (1, 5), (1, 6), (1, 7)
]

STARTING_POSITIONS_FOR_B_PAWNS = [
    (6, 0), (6, 1), (6, 2), (6, 3),
    (6, 4), (6, 5), (6, 6), (6, 7)
]

PLAYER_VALUES: dict[PieceColor, float] = {
    PieceColor.WHITE: 1,
    PieceColor.BLACK: -1
}
