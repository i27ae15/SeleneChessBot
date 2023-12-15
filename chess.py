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

    # print(
    #     board.get_attacked_squares(
    #         color=PieceColor.WHITE,
    #         show_in_algebraic_notation=True
    #     )
    # )

    rooks = board.get_piece(
        piece_name=PieceName.ROOK,
        color=PieceColor.WHITE
    )

    # eliminate the pawns in front of the rooks
    board.board[1][0] = None
    board.board[1][7] = None

    for rook in rooks:
        legal_moves = rook.calculate_legal_moves()
        rook.move_to(new_position=legal_moves[0])

    # print(p.calculate_legal_moves(show_in_algebraic_notation=True))


if __name__ == "__main__":
    main()
