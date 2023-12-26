from core.utils import convert_from_algebraic_notation

from board import Board

from pieces.utilites import PieceColor, PieceName
from pieces import Piece


class Game:

    def __init__(self) -> None:
        """
        This class will be the main class of the game.

        It will be responsible for:

        - Creating the board
        - Track the moves of the game
        - Track the following rules:
            * the 50 moves rule
            * the 3-fold repetition rule
            * the insufficient material rule
            * stalemate
            * checkmate

        The board and game class will live independently from each other.
        So there can be a board without a game and a game without a board.

        """

        self.board: Board = Board()
        self.moves: dict = {}

        """
        The dict will look like this:

        {
            #N: [Move 1, Move 2]
        }

        Where the first element of the list if the move for white and the
        second for the black player

        """

        self.player_turn: PieceColor = PieceColor.WHITE

        self.current_turn: int = 1

    def move_piece(self, move: str) -> None:
        """
        This method will add a move to the moves dict.

        :param move: The move in algebraic notation
        :param player: The player that made the move
        :return: None

        Note: we should add a P in front when a pawn is being moved

        """

        piece_abbreviation = move[0]
        square = move[1:]

        pieces = self.board.pieces_on_board[self.player_turn]
        piece: Piece = self._get_movable_piece(
            piece_name=piece_abbreviation,
            move_to=square,
            pieces=pieces
        )

        piece.move_to(square)
        piece.add_move_to_story(
            move_number=self.current_turn,
            new_position=square
        )

        # check if the move is valid

        if self.current_turn not in self.moves:
            self.moves[self.current_turn] = []

        self.player_turn = self.player_turn.opposite()

        if piece_abbreviation == 'P':
            move = move[1:]
        self.moves[self.current_turn].append(move)

        if self.player_turn == PieceColor.WHITE:
            self.current_turn += 1

    def _get_movable_piece(
        self,
        piece_name: str,
        move_to: str,
        pieces: dict[list[Piece]]
    ) -> Piece | None:
        """
        This method will return the piece that can be moved.

        :param pieces: The pieces that can be moved
        :return: The piece that can be moved

        """
        piece_name = self._get_piece_name_class(piece_name)
        pieces = pieces[piece_name]

        # get the piece that can move to the given square
        move_to = convert_from_algebraic_notation(move_to)

        for piece in pieces:
            piece: Piece
            if move_to in piece.calculate_legal_moves():
                return piece

        raise ValueError('Invalid move')

    def _get_piece_name_class(self, move: str) -> PieceName:
        for piece in PieceName:
            # Check if the move matches the abbreviation of the piece
            if piece.value[1] == move:
                return piece  # Return the full name of the piece
        raise ValueError('Invalid piece abbreviation')
