import random

from board import Board

from pieces.utilites import PieceColor, PieceName, RookSide
from pieces import Piece, Pawn, King

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
        self.moves_for_f_rule: int = 0
        self.board_states: dict[str] = dict()

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

        self.is_game_terminated: bool = False
        self.is_game_drawn: bool = False
        self.zobrist_keys: dict = None

        self._initialize_zobrist_keys()

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

        piece_move = PieceMove(
            move=move,
            player_turn=self.player_turn,
            board=self.board
        )

        self._add_board_state()

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

        self._manage_fifty_moves_rule(piece_move)

        # manage the game_state
        self._manage_game_state(piece_move)

    def _initialize_zobrist_keys(self):

        if self.zobrist_keys:
            return

        keys = {}
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
        for piece in pieces:
            keys[piece] = {}
            for row in range(8):
                for column in range(8):
                    keys[piece][(row, column)] = random.getrandbits(64)

        keys['castling'] = {
            (PieceColor.WHITE, RookSide.KING): random.getrandbits(64),
            (PieceColor.WHITE, RookSide.QUEEN): random.getrandbits(64),
            (PieceColor.BLACK, RookSide.KING): random.getrandbits(64),
            (PieceColor.BLACK, RookSide.QUEEN): random.getrandbits(64)
        }
        keys['en_passant'] = {
            column: random.getrandbits(64) for column in range(8)
        }  # Assuming column index for en passant
        keys['side'] = random.getrandbits(64)

        self.zobrist_keys = keys

    def compute_board_hash(
        self,
        board: Board,
        current_side: PieceColor,
        castling_rights: dict,
        en_passant_column: dict
    ) -> int:

        board_hash = 0

        # Iterate through each piece on the board and XOR its key
        for row in range(8):
            for column in range(8):
                piece = board.get_square_or_piece(row, column)
                if isinstance(piece, Piece):
                    piece: Piece
                    piece_key = self.zobrist_keys[piece.name.value[1]][(row, column)]
                    board_hash ^= piece_key

        # Include castling rights
        for side, rights in castling_rights.items():
            for right, enabled in rights.items():
                if enabled:
                    board_hash ^= self.zobrist_keys['castling'][(side, right)]

        # Include en passant possibility
        if en_passant_column is not None:
            board_hash ^= self.zobrist_keys['en_passant'][en_passant_column]

        # Include the side to move
        if current_side == PieceColor.BLACK:
            board_hash ^= self.zobrist_keys['side']

        return board_hash

    def _add_board_state(self):

        en_passant_column = (
            self.black_possible_pawn_enp or self.white_possible_pawn_enp
        )

        if en_passant_column:
            en_passant_column = en_passant_column.column

        board_hash = self.compute_board_hash(
            current_side=self.player_turn,
            board=self.board,
            castling_rights=self.board.castleling_rights,
            en_passant_column=en_passant_column
        )

        if board_hash in self.board_states:
            st = self.board_states[board_hash]
            self.board_states[board_hash] = st + 1
            if st + 1 >= 3:
                self.is_game_terminated = True
                self.is_game_drawn = True
        else:
            self.board_states[board_hash] = 1

    def print_game_state(self):
        """
        Prints the current state of the game.

        This method prints the current state of the game, including the
        current player turn, the move history, and the board.
        """

        print(f'Player turn: {self.player_turn}')
        print(f'white king in check: {self.board.white_king.is_in_check}')
        print(f'black king in check: {self.board.black_king.is_in_check}')
        print(f'is_game_terminated: {self.is_game_terminated}')
        print(f'moves_for_f_rule: {self.moves_for_f_rule}')

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

    def _manage_fifty_moves_rule(self, piece_move: PieceMove):
        """
        Manages the 50 moves rule.

        This method manages the 50 moves rule, which states that a game is
        drawn if no capture has been made and no pawn has been moved in the
        last 50 moves. It tracks the number of moves since the last capture
        or pawn move and resets the counter if either of these conditions are
        met.

        Parameters:
            piece_move (PieceMove): The move that has just been executed.
        """

        if piece_move.piece_name == PieceName.PAWN:
            self.moves_for_f_rule = 0
        elif piece_move.is_capture:
            self.moves_for_f_rule = 0
        else:
            self.moves_for_f_rule += 1

        if self.moves_for_f_rule >= 100:
            self.is_game_terminated = True

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

        self._manage_check_detection()
        self._manage_game_termination()

        # check if the move is valid
        if self.current_turn not in self.moves:
            self.moves[self.current_turn] = []

        self.player_turn = self.player_turn.opposite()
        self.moves[self.current_turn].append(piece_move.move)

        if self.player_turn == PieceColor.WHITE:
            self.current_turn += 1

        self.board._attacked_squares_by_white_checked = False
        self.board._attacked_squares_by_black_checked = False

    def _manage_check_detection(self):
        """
        Manages the detection of check and checkmate.

        This method checks if the move has caused a check or checkmate. If
        so, it raises an error, indicating the end of the game.

        Parameters:
            piece_move (PieceMove): The move that has just been executed.

        Raises:
            ValueError: If the move has caused a check or checkmate.
        """

        self.board.white_king.check_if_in_check()
        self.board.black_king.check_if_in_check()

    def _manage_game_termination(self) -> bool:
        """
        Manages the termination of the game.

        This method checks if the move has caused the game to end, either
        through checkmate or stalemate. If so, it raises an error, indicating
        the end of the game.

        Parameters:
            piece_move (PieceMove): The move that has just been executed.

        Raises:
            ValueError: If the move has caused the game to end.
        """

        king: King = self.board.get_piece(
            piece_name=PieceName.KING,
            color=self.player_turn.opposite()
        )[0]

        if king.is_in_check:
            # check if there are legal moves in the board for the color
            if not self._color_has_legal_moves(
                color=king.color,
                is_king_in_check=True
            ):
                self.is_game_terminated = True

        # check if there is a stale mate in the board
        # the minimum pieces that are required for a stalemate are 8]

        n_pieces = [
            self.board.n_white_pieces,
            self.board.n_black_pieces
        ]

        n_pieces = n_pieces[king.color.value]

        if not king.is_in_check and n_pieces <= 8:
            if not self._color_has_legal_moves(
                color=king.color,
                is_king_in_check=False
            ):
                self.is_game_terminated = True

    def _color_has_legal_moves(
        self,
        color: PieceColor,
        is_king_in_check: bool
    ) -> bool:
        """
        Checks if a color has legal moves.

        This method checks if the given color has any legal moves left. It
        does so by iterating through all the pieces of the color and checking
        if any of them have legal moves.

        Parameters:
            color (PieceColor): The color to check for legal moves.

        Returns:
            bool: True if the color has legal moves, False otherwise.
        """

        # first we need to check for the king

        king: King = self.board.get_piece(
            piece_name=PieceName.KING,
            color=color
        )[0]

        king_moves = king.calculate_legal_moves()

        if king_moves:
            return True

        if is_king_in_check:
            return self._check_legal_moves_when_king_is_in_check(king)

        elif not is_king_in_check:
            return self._check_legal_moves_when_king_is_not_in_check(color)

    def _check_legal_moves_when_king_is_not_in_check(
        self,
        color: PieceColor
    ):
        for piece_key in self.board.pieces_on_board[color]:
            for piece in self.board.pieces_on_board[color][piece_key]:
                piece: Piece
                if piece.calculate_legal_moves():
                    return True

    def _check_legal_moves_when_king_is_in_check(
        self,
        king: King
    ) -> bool:

        # if the king does not have legal moves, we need to check if there is a
        # piece that can protect the king from being attacked
        # first we need to knwo what is the piece that is attacking the king

        # get the pieces that are attacking the king
        # since we calculated that above, the variable pieces_attacking_me
        # should be filled

        pieces: list[Piece] = king.pieces_attacking_me['pieces']

        for piece in pieces:
            # look first for a knight or a pawn
            if piece.name in (PieceName.KNIGHT, PieceName.PAWN):
                # this will mean that the only way to protect the king is to
                # capture the piece
                # so we need to check if there is a piece that can capture
                # the attacking pawn or knight

                pos_to_cap = self._check_if_piece_can_capture_attacking_piece(
                    attacking_piece=piece,
                    king=king
                )

                if pos_to_cap:
                    # this mean checkmate
                    # this was not pos and return False
                    return True

            else:
                # this mean that the attacking piece is a bishop, a rook or a
                # queen. For this pieces we have two options:
                # 1. capture the attacking piece
                # 2. put a piece between the attacking piece and the king

                pos_to_cap = self._check_if_piece_can_capture_attacking_piece(
                    attacking_piece=piece,
                    king=king
                )

                if pos_to_cap:
                    return True

                # now we need to check if there is a piece that can be put
                # between the attacking piece and the king
                # the best approach if to identify where is the piece that is
                # attacking the king once we know this, we should scan, row,
                # column and diagonal and look for a piece
                # that can move to the position blocking the attacked

                pos_to_block = self._check_if_piece_can_block_attacking_piece(
                    attacking_piece=piece,
                    king=king
                )

                if pos_to_block:
                    return True

        return False

    def _check_if_piece_can_capture_attacking_piece(
        self,
        attacking_piece: Piece,
        king: King
    ):

        pieces = self.board.pieces_on_board[king.color]

        for piece_key in pieces:
            for piece in pieces[piece_key]:
                piece: Piece
                if attacking_piece in piece.get_pieces_under_attack():
                    return True

        return False

    def _check_if_piece_can_block_attacking_piece(
        self,
        attacking_piece: Piece,
        king: King
    ) -> bool:

        # first check if the king is being double attacked
        # if so, we can not block the attack

        if len(king.pieces_attacking_me['pieces']) > 1:
            return False

        pieces = self.board.pieces_on_board[king.color]

        # first identify where is the piece that is attacking the king
        # this means if a row, column or diagonal

        rc_directions = ['d0', 'd1']
        d_directions = ['d0', 'd1', 'd2', 'd3']

        possible_blocking_squares = []

        if attacking_piece.row == king.row:
            # here this means the king and the attacking piece are
            # in the same row, so the attacking square can be either
            # a rook or a queen, let's scan the row and get for the
            # possible squares where another piece can go to blcok

            row = king.scan_row()

            for dir in rc_directions:
                if not row[dir]:
                    continue
                last_pos = row[dir][-1]
                if last_pos == attacking_piece:
                    if row[dir]:
                        possible_blocking_squares = row[dir]
                        break

        elif attacking_piece.column == king.column:

            column = king.scan_column()

            for dir in rc_directions:
                if not column[dir]:
                    continue
                last_pos = column[dir][-1]
                if last_pos == attacking_piece:
                    if column[dir]:
                        possible_blocking_squares = column[dir]
                        break

        else:

            # at this point we know that the piece is in a diagonal

            diagonal = king.scan_diagonals()

            for dir in d_directions:
                if not diagonal[dir]:
                    continue
                last_pos = diagonal[dir][-1]
                if last_pos == attacking_piece:
                    if diagonal[dir]:
                        possible_blocking_squares = diagonal[dir]
                        break

        for piece_key in pieces:
            for piece in pieces[piece_key]:
                piece: Piece
                for possible_square in possible_blocking_squares:
                    if possible_square in piece.calculate_legal_moves():
                        return True

        return False
