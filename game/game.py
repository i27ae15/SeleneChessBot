
from board import Board

from pieces.utilites import PieceColor, PieceName
from pieces import Piece, Pawn

from .piece_move import PieceMove


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

        self.white_possible_pawn_enp: Pawn | None = None
        self.black_possible_pawn_enp: Pawn | None = None

        self.en_passant_pawns = {
            PieceColor.WHITE: self.white_possible_pawn_enp,
            PieceColor.BLACK: self.black_possible_pawn_enp
        }

    def move_piece(self, move: str) -> None:
        """
        This method will add a move to the moves dict.

        :param move: The move in algebraic notation
        :return: None

        Note: we should add a P in front when a pawn is being moved
        """

        piece_move = PieceMove(move, self.player_turn)

        pieces = self.board.pieces_on_board[self.player_turn]
        piece: Piece = self._get_movable_piece(
            piece=piece_move.piece,
            move_to=piece_move.square,
            pieces=pieces
        )

        if piece_move.is_castleling:
            if not piece.castle(side=piece_move.castleling_side):
                raise ValueError('Invalid move')
        else:
            if not piece.move_to(piece_move.square):
                raise ValueError('Invalid move')

        en_passant_pawn: Pawn = self.en_passant_pawns[self.player_turn]

        # set the last pawn moved two squares to not be able to be captured
        if en_passant_pawn:
            en_passant_pawn.can_be_captured_en_passant = False

            if self.player_turn == PieceColor.WHITE:
                self.white_possible_pawn_enp = None
            elif self.player_turn == PieceColor.BLACK:
                self.black_possible_pawn_enp = None

        # if the piece is a pawn, track for en passant
        if piece_move.piece == PieceName.PAWN:
            piece: Pawn
            # if the move is a double move, track the pawn
            if piece_move.square[-1] in '45':

                if self.player_turn == PieceColor.WHITE:
                    self.white_possible_pawn_enp = piece
                elif self.player_turn == PieceColor.BLACK:
                    self.black_possible_pawn_enp = piece

                piece.can_be_captured_en_passant = True

        piece.add_move_to_story(
            move_number=self.current_turn,
            new_position=piece_move.square
        )

        # check if the move is valid

        if self.current_turn not in self.moves:
            self.moves[self.current_turn] = []

        self.player_turn = self.player_turn.opposite()
        self.moves[self.current_turn].append(piece_move.move)

        if self.player_turn == PieceColor.WHITE:
            self.current_turn += 1

    def _get_movable_piece(
        self,
        piece: PieceName,
        move_to: str,
        pieces: dict[list[Piece]]
    ) -> Piece | None:
        """
        This method will return the piece that can be moved.

        :param pieces: The pieces that can be moved
        :return: The piece that can be moved

        """
        pieces = pieces[piece]
        # get the piece that can move to the given square

        for piece in pieces:
            piece: Piece

            if move_to in piece.calculate_legal_moves(
                show_in_algebraic_notation=True
            ):
                return piece

        raise ValueError('Invalid move')
