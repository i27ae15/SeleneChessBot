# chess.py
from board import Board
from pieces import Pawn
from pieces.king import King
from pieces.utilites import PieceName, PieceColor

# Import other necessary modules and classes


def main():
    board = Board()
    # print(board)
    # board.add_piece(Pawn(PieceColor.BLACK, (2, 5), board=board))
    # p = King(PieceColor.WHITE, (4, 7), board=board)
    # board.add_piece(piece=p)

    # print(board)
    # print(board.pieces_on_board)
    print(board.get_piece(piece_name=PieceName.KING, piece_color=PieceColor.WHITE))

    # print(p.calculate_legal_moves(show_in_algebraic_notation=True))


if __name__ == "__main__":
    main()
