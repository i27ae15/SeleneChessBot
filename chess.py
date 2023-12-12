# chess.py
from board import Board
from pieces import Pawn
from pieces.utilites import PieceColor

# Import other necessary modules and classes


def main():
    # Create a board instance, set up the game, etc.
    board = Board()
    # print(board)
    board.add_piece(Pawn(PieceColor.BLACK, (2, 5), board=board))
    board.add_piece(Pawn(PieceColor.BLACK, (2, 3), board=board))
    print(board)

    print(board.board[1][4].calculate_legal_moves(
            show_in_algebraic_notation=True
        )
    )


if __name__ == "__main__":
    main()
