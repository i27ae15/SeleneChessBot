# chess.py
from board import Board
from pieces import Pawn
from pieces.king import King
from pieces.utilites import PieceColor

# Import other necessary modules and classes


def main():
    board = Board()
    # print(board)
    # board.add_piece(Pawn(PieceColor.BLACK, (2, 5), board=board))
    # p = King(PieceColor.WHITE, (4, 7), board=board)
    # board.add_piece(piece=p)

    print(board)
    print(board.pieces_on_board)
    # print(p.calculate_legal_moves(show_in_algebraic_notation=True))


if __name__ == "__main__":
    main()
