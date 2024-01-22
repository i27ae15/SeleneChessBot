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


class PieceValue(Enum):
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
    KING = float('inf')


class PieceName(Enum):
    PAWN = 'Pawn', 'P',
    BISHOP = 'Bishop', 'B'
    KNIGHT = 'Knight', 'N'
    ROOK = 'Rook', 'R'
    QUEEN = 'Queen', 'Q'
    KING = 'King', 'K'


class RookSide(Enum):
    QUEEN = 0
    KING = 1


NO_TRASPASS_KING_PIECES = [
    PieceName.PAWN,
    PieceName.KING,
    PieceName.KNIGHT
]