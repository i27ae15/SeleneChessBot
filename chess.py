# chess.py
from board import Board
from pieces import Pawn
from pieces.king import King
from pieces.utilites import PieceName, PieceColor, RookSide

# Import other necessary modules and classes


def main():
    board = Board()
    # print(board)
    # board.add_piece(Pawn(PieceColor.BLACK, (2, 5), board=board))
    # p = King(PieceColor.WHITE, (4, 7), board=board)
    # board.add_piece(piece=p)

    # print(
    #     board.get_attacked_squares(
    #         color=PieceColor.WHITE,
    #         show_in_algebraic_notation=True
    #     )
    # )

    king: King = board.get_piece(
        piece_name=PieceName.KING,
        color=PieceColor.WHITE
    )[0]

    # eliminate the pawns in front of the rooks

    print(board)

    # eliminate the pieces between the king and the king side rook
    board.board[0][5] = None
    board.board[0][6] = None

    # eliminate the pieces between the king and the queen side rook
    board.board[0][1] = None
    board.board[0][2] = None
    board.board[0][3] = None

    king.castle(side=RookSide.QUEEN)

    # do the same but for the black king

    king: King = board.get_piece(
        piece_name=PieceName.KING,
        color=PieceColor.BLACK
    )[0]

    # eliminate the pieces between the king and the king side rook
    board.board[7][5] = None
    board.board[7][6] = None

    # eliminate the pieces between the king and the queen side rook
    board.board[7][1] = None
    board.board[7][2] = None
    board.board[7][3] = None

    king.castle(side=RookSide.QUEEN)

    print(board)


if __name__ == "__main__":
    main()
