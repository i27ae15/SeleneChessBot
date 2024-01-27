
from board import Board

from pieces.utilites import PieceColor, PieceName
from pieces import Piece, Pawn

from .piece_move import PieceMove


class Game:

    """
    This class represents the main controller of a chess game.

    It will be responsible for:

        - Creating the board
        - Track the moves of the game
        - Track the following rules:
            * the 50 moves rule
            * the 3-fold repetition rule
            * the insufficient material rule
            * stalemate
            * checkmate

    The Game class operates independently from the Board class, allowing for
    the existence of a board without a game and vice versa.

    Attributes:
        board (Board): An instance of the Board class representing the
        chessboard.

        moves (dict): A dictionary tracking all moves made in the game,
        structured with turn numbers as keys and lists of moves
        (first White, then Black) as values.

        player_turn (PieceColor): The color of the player whose turn it is to
        move.

        current_turn (int): The current turn number in the game.

        white_possible_pawn_enp (Pawn | None): Tracks the White pawn eligible
        for en passant.

        black_possible_pawn_enp (Pawn | None): Tracks the Black pawn eligible
        for en passant.

        en_passant_pawns (dict): A dictionary mapping each player color to
        their pawn that can potentially be captured en passant.

    Methods:

        move_piece(move: str) -> None:
            Processes and adds a move to the game, updating the board and game
            state accordingly.

        _get_movable_piece(
                piece_move: PieceMove,
                pieces: dict[list[Piece]]
            ) -> Piece | None:
            Determines and returns the specific piece that is to be moved
            based on the provided move information.

        _manage_game_state(piece_move: PieceMove) -> None:
            Updates the game state after each move, including turn
            management and move tracking.

        _move_piece(piece: Piece, piece_move: PieceMove) -> None:
            Executes a chess piece's move on the board, including handling
            special moves.

        _clean_en_passant_pawns(piece: Piece, piece_move: PieceMove) -> None:
            Resets en passant status of pawns after a move.

        _manage_en_passant_pawns(piece: Piece, piece_move: PieceMove) -> None:
            Manages potential en passant captures based on recent pawn moves.
    """

    def __init__(self) -> None:

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

    def move_piece(self, move: str) -> None:
        """
        Processes a chess move and updates the game state accordingly.

        This method interprets the given move in algebraic notation and
        applies it to the game. It handles various aspects of a chess move
        including piece movement, castling, and pawn-specific rules like en
        passant. After executing the move, it updates the game's state by
        switching the player turn, tracking the move history, and preparing
        for the next turn. Additionally, it ensures that moves adhere to the
        rules of chess, raising an error for invalid moves.

        Parameters:
            move (str): The chess move in algebraic notation.

        Raises:
            ValueError: If the move is determined to be invalid or illegal in
            the current game state.
        """

        piece_move = PieceMove(move, self.player_turn)

        pieces = self.board.pieces_on_board[self.player_turn]
        piece: Piece = self._get_movable_piece(
            piece_move=piece_move,
            pieces=pieces[piece_move.piece_name]
        )

        # move the piece
        # manage the en passant pawns
        self._manage_en_passant_pawns(piece, piece_move)

        self._move_piece(piece, piece_move)

        self._manage_coronation(piece, piece_move)

        piece.add_move_to_story(
            move_number=self.current_turn,
            new_position=piece_move.square
        )

        # manage the game_state
        self._manage_game_state(piece_move)

    def _clean_en_passant_state(self):
        """
        Resets the en passant status of pawns.

        This method is called after each move to ensure that the en passant
        capture opportunity is only available for one turn after a pawn moves
        two squares forward from its starting position.
        """

        en_passant_pawn: Pawn = None

        if self.player_turn == PieceColor.WHITE:
            en_passant_pawn = self.white_possible_pawn_enp
        elif self.player_turn == PieceColor.BLACK:
            en_passant_pawn = self.black_possible_pawn_enp

        # set the last pawn moved two squares to not be able to be captured

        if en_passant_pawn:
            en_passant_pawn.can_be_captured_en_passant = False

            if self.player_turn == PieceColor.WHITE:
                self.white_possible_pawn_enp = None
            elif self.player_turn == PieceColor.BLACK:
                self.black_possible_pawn_enp = None

    def _manage_en_passant_pawns(self, piece: Piece, piece_move: PieceMove):
        """
        Manages pawns that can be captured en passant.

        This method updates the tracking of pawns eligible for en passant
        capture, based on the most recent move. It first clears the current
        en passant status and then sets up new pawns for en passant if
        applicable.

        Parameters:
            piece (Piece): The piece that has just been moved, potentially
            a pawn.
            piece_move (PieceMove): The move that has just been executed.
        """

        self._clean_en_passant_state()

        # if the piece is a pawn, track for en passant
        if piece_move.piece_name == PieceName.PAWN:
            piece: Pawn
            # if the move is a double move, track the pawn
            if piece_move.square[-1] in '45' and piece.first_move:

                if self.player_turn == PieceColor.WHITE:
                    self.white_possible_pawn_enp = piece
                elif self.player_turn == PieceColor.BLACK:
                    self.black_possible_pawn_enp = piece

                piece.can_be_captured_en_passant = True

    def _manage_coronation(self, piece: Piece, piece_move: PieceMove):
        """
        Manages the coronation of a pawn.

        This method handles the coronation of a pawn into a queen. It checks
        if the move is a pawn move that reaches the last row of the board,
        and if so, it replaces the pawn with a queen.

        Parameters:
            piece (Piece): The piece that has just been moved, potentially
            a pawn.

            piece_move (PieceMove): The move that has just been executed.
        """

        if isinstance(piece, Pawn) and piece_move.coronation_into:
            piece.coronate(piece_move.coronation_into)

    def _get_movable_piece(
        self,
        piece_move: PieceMove,
        pieces: dict[list[Piece]]
    ) -> Piece | None:
        """
        Identifies and returns the specific piece that can legally perform the
        given move.

        This method iterates through the provided list of pieces, filtering
        them based on the requirements of the move (such as the piece's file
        or position). It then checks if the move is within the piece's legal
        moves. The method is crucial for ensuring that only valid and legal
        chess moves are executed in the game. If no piece matches the criteria
        for the move, it raises an error, indicating an illegal move.

        Parameters:
            piece_move (PieceMove): The parsed move information, encapsulating
            details like the piece type and target square.

            pieces (dict[list[Piece]]): A dictionary of pieces keyed by their
            types, available for moving.

        Returns:
            Piece | None: The piece that is eligible and able to make the move.

        Raises:
            ValueError: If no eligible piece is found or if the move is
            illegal.
        """

        for piece in pieces:
            piece: Piece

            # if there is a file in the piece_move object, look for that file
            # when going to the piece, so we do not have to calculate the legal
            # moves for all the pieces

            if piece_move.piece_file:
                if piece.algebraic_pos[0] != piece_move.piece_file:
                    continue

            # check if the row is given
            if piece_move.row is not None:
                if piece.row != piece_move.row:
                    continue

            # if we are here, we have found the piece (two pieces can be in
            # the same file) or we do not have a file, so calculate the legal
            # moves for the piece and check if the move is in the legal moves

            if piece_move.square in piece.calculate_legal_moves(
                show_in_algebraic_notation=True
            ):
                return piece

        raise ValueError('Invalid move')

    def _move_piece(self, piece: Piece, piece_move: PieceMove):
        """
        Executes the movement of a piece on the board.

        This method handles the actual movement of a piece, including special
        moves like castling. It ensures that the piece is moved according to
        the rules of chess, raising an error if the move is invalid.

        Parameters:
            piece (Piece): The piece to be moved.
            piece_move (PieceMove): The move to be executed.

        Raises:
            ValueError: If the move is not legal or possible.
        """

        if piece_move.is_castleling:
            # this mean that the piece is the king
            if not piece.castle(side=piece_move.castleling_side):
                raise ValueError('Invalid move')
        else:
            if not piece.move_to(piece_move.square):
                raise ValueError('Invalid move')

    def _manage_game_state(self, piece_move: PieceMove):
        """
        Manages the state of the game after a move is made.

        This method updates the game's move history and player turns. It
        ensures that the moves are recorded correctly and manages the
        transition between turns. It also increments the turn counter when
        it's time for the White player to move again.

        Parameters:
            piece_move (PieceMove): The move that has just been executed.
        """
        # check if the move is valid
        if self.current_turn not in self.moves:
            self.moves[self.current_turn] = []

        self.player_turn = self.player_turn.opposite()
        self.moves[self.current_turn].append(piece_move.move)

        if self.player_turn == PieceColor.WHITE:
            self.current_turn += 1
            # TODO: Look for a better way to reset these variables
        self.board._attacked_squares_by_white_checked = False
        self.board._attacked_squares_by_black_checked = False
