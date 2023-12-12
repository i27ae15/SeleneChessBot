# chess.py
from board import Board
from pieces import Rook
from pieces import Pawn
from pieces.utilites import PieceColor

# Import other necessary modules and classes


def main():
    board = Board()
    # print(board)
    # board.add_piece(Pawn(PieceColor.BLACK, (2, 5), board=board))
    r = Rook(PieceColor.WHITE, (3, 3), board=board)
    board.add_piece(piece=r)

    # print(board.board[6][4].calculate_legal_moves(
    #         show_in_algebraic_notation=True
    #     )
    # )

    print(board)
    print(r.calculate_legal_moves(show_in_algebraic_notation=True))

    # print(a_rook.scan_column(end_at_piece_found=False))
    # print(a_rook.scan_row(end_at_piece_found=False))


if __name__ == "__main__":
    main()
