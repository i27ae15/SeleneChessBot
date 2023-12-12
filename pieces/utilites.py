from enum import Enum


class PieceColor(Enum):
    WHITE = 0
    BLACK = 1


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
