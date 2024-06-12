import random

from core.singleton import SingletonMeta

from pieces.utilites import PieceColor, RookSide


class ZobristHash(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.keys: dict = self._initialize_zobrist_keys()

    def _initialize_zobrist_keys(self) -> dict:

        random.seed(42)

        keys = {}
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K']
        for piece in pieces:
            keys[piece] = {
                PieceColor.WHITE: {},
                PieceColor.BLACK: {}
            }
            for c in range(2):
                color = PieceColor(c)
                for row in range(8):
                    for column in range(8):
                        keys[piece][color][(row, column)] = random.getrandbits(64)

        keys['castling'] = {
            (PieceColor.WHITE, RookSide.KING): random.getrandbits(64),
            (PieceColor.WHITE, RookSide.QUEEN): random.getrandbits(64),
            (PieceColor.BLACK, RookSide.KING): random.getrandbits(64),
            (PieceColor.BLACK, RookSide.QUEEN): random.getrandbits(64)
        }
        keys['en_passant'] = {
                PieceColor.WHITE: {
                    column: random.getrandbits(64) for column in range(8)
                },
                PieceColor.BLACK: {
                    column: random.getrandbits(64) for column in range(8)
                }
        }  # Assuming column index for en passant

        keys['side'] = {
            PieceColor.WHITE: random.getrandbits(64),
            PieceColor.BLACK: random.getrandbits(64)
        }

        return keys


# Initialize the ZobristHash singleton
__zobrist_hash__ = ZobristHash()
ZOBRIEST_KEYS = __zobrist_hash__.keys
