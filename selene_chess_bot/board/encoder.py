import numpy as np

from typing import TYPE_CHECKING

from core.singleton import SingletonMeta

from pieces import Piece
from pieces.utilites import PieceName, PieceColor

from board.types import BoardRepresentation


if TYPE_CHECKING:
    from board import Board


class BoardEncoder(metaclass=SingletonMeta):

    @staticmethod
    def encode_board(
        board: 'Board'
    ) -> np.ndarray:

        """
            Encode the chess board state into a 3D numpy array with shape
            (8, 8, 12)
        """

        board_state = np.zeros((8, 8, 12), dtype=np.uint8)

        piece_to_channel = {
            PieceName.PAWN: 0,
            PieceName.KNIGHT: 1,
            PieceName.BISHOP: 2,
            PieceName.ROOK: 3,
            PieceName.QUEEN: 4,
            PieceName.KING: 5
        }

        board_representation: BoardRepresentation = board.board

        for row_index, row in enumerate(board_representation):
            for column_index, piece in enumerate(row):

                piece: Piece = board.get_square_or_piece(
                    row=row_index,
                    column=column_index
                )

                if isinstance(piece, Piece):
                    channel = piece_to_channel[piece.name]
                    if piece.color == PieceColor.BLACK:
                        channel += 6

                    board_state[row_index, column_index, channel] = 1

        return board_state

    @staticmethod
    def visualize_encoded_board(encoded_board: np.ndarray) -> None:
        piece_to_channel = {
            PieceName.PAWN: 0,
            PieceName.KNIGHT: 1,
            PieceName.BISHOP: 2,
            PieceName.ROOK: 3,
            PieceName.QUEEN: 4,
            PieceName.KING: 5
        }

        inverse_piece_to_channel = {v: k for k, v in piece_to_channel.items()}

        for row_index in range(8):
            for column_index in range(8):
                piece = None
                color = ''

                for channel in range(12):
                    if encoded_board[row_index, column_index, channel] == 1:
                        piece = inverse_piece_to_channel.get(channel % 6)
                        color = 'B' if channel >= 6 else 'W'
                        break

                if piece:
                    print(f"{piece.value[1]}{color}", end=' ')
                else:
                    print('0', end=' ')
            print()


__board_encoder__ = BoardEncoder()
