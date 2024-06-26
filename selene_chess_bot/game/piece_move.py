from core.utils import convert_from_algebraic_notation

from pieces.utilites import PieceColor, PieceName, RookSide
from pieces import Piece

from board import Board

from game.exceptions import InvalidMoveError


class PieceMove:
    """
    Represents a chess move in a game.

    This class processes and stores detailed information about a chess
    move, including the type of piece moved, the move's notation, and
    the player's turn. It also handles special moves like castling and
    determines the target square and piece position based on algebraic
    chess notation.

    Important: This class does not check whether the move is legal or
    not. It only processes the move string and stores the information
    about the move.

    Attributes:
        move (str): The move in standard algebraic notation.

        player_turn (PieceColor): Indicates which player
        (White or Black) made the move.

        is_castling (bool): True if the move is a castling move, False
        otherwise.

        castling_side (RookSide | None): Indicates the side
        (King or Queen) of castling if applicable.

        piece_abbreviation (str | None): The abbreviation of the moved
        piece (e.g., 'P' for Pawn).

        piece (PieceName | None): The name of the moved piece
        (e.g., PieceName.PAWN).

        piece_file (str | None): The file (column) of the moved piece,
        relevant for pawn moves.

        square (str | None): The target square of the move
        in algebraic notation.

        _abr_move (str): A cleaned version of the move string,
        stripped of special characters.

    Methods:
        set_piece(look_for_pawn: bool) -> PieceName:
            Determines and sets the piece involved in the move,
            based on the move notation.

        get_castling_square() -> str:
            Calculates the target square for a castling move.

        set_square_and_pos():
            Determines and sets the target square and the position of
            the piece.

        set_move_information():
            Parses the move string to extract and set detailed move
            information.
        """

    def __init__(
        self,
        move: str,
        board: Board,
        player_turn: PieceColor,
    ) -> None:
        """
        Initializes the PieceMove instance with the given move and player's
        turn.

        Parses the provided move string to determine the basic characteristics
        of the move, such as whether it involves castling, the piece involved,
        and the target square. Also initializes other attributes to store
        move details.

        Parameters:
            move (str): The chess move in standard algebraic notation.
            player_turn (PieceColor): The color (White or Black) of the player
            making the move.


        NOTE: If there is a bug, firs look into "move_to_compare" property
        """

        # Move ---------------------
        self.move: str = move
        self._abr_move: str = None

        # Piece ---------------------
        self.is_capture: bool = False
        self.piece_file: str | None = None
        self.piece_name: PieceName | None = None
        self.piece_abbreviation: str | None = None
        self.coronation_into: PieceName | None = None

        # Square ---------------------
        self.row: int | None = None
        self.square: str | None = None
        self.square_pos: tuple[int, int] | None = None

        # Player ---------------------
        self.is_castleling: bool = False
        self.player_turn: PieceColor = player_turn
        self.castleling_side: RookSide | None = None

        # Board ---------------------
        self.board: Board = board

        # Initialize the move information
        self._set_abreviate_move()
        self._set_move_information()

    @property
    def move_to_compare(self) -> str:
        if self.piece_name == PieceName.PAWN:
            if self.coronation_into:
                # NOTE: Be careful because in the future we may have
                # to change this
                return self.move.replace('+', '').replace('#', '')

        return self.square

    # ---------------------------- SETTER METHODS -----------------------------

    def _set_move_information(self):
        """
        Parses the move string to extract and set detailed move information.

        This method is a comprehensive handler that sets the piece type, the
        target square, and other move-specific details. It is responsible for
        ensuring that all relevant attributes of the move are accurately
        determined and set.

        Raises:
            ValueError: If the move notation is invalid or cannot be parsed.
        """
        # if we haven't get the piece yet, let's get it here
        self._set_piece()

        # we now have to get the square where the piece is being move to
        # and the pos of the piece if given
        self._set_square_and_pos()

        # see if the piece is being coronated
        self._set_coronation()

        # see if the move is a capture
        self._set_is_capture()

    def _set_piece(self):
        """
        Determines and sets the type of piece involved in the move.

        This method analyzes the move's notation to identify the piece type,
        handling special cases like pawn moves and castling. If the piece
        cannot be determined from the notation, it raises a ValueError.

        Parameters:
            look_for_pawn (bool): If True, the method checks if the move is by
            a pawn.

        Returns:
            PieceName: The enum representing the type of piece involved in the
            move.

        Raises:
            ValueError: If the move notation does not correspond to a valid
            piece.
        """

        if len(self._abr_move) == 2 or self._abr_move[0] in 'abcdefgh':
            # this will mean that the piece is a pawn
            self.piece_abbreviation = PieceName.PAWN.value[1]
            self.piece_name = PieceName.PAWN

        elif self._abr_move == 'O-O' or self._abr_move == 'O-O-O':
            # the piece we want to move is the king
            self.is_castleling = True
            self.piece_abbreviation = PieceName.KING.value[1]
            self.piece_name = PieceName.KING
        else:
            abr = self._abr_move[0]
            for piece in PieceName:
                if piece.value[1] == abr:
                    self.piece_abbreviation = piece.value[1]
                    self.piece_name = piece
                    break
            else:
                raise InvalidMoveError('_set_piece')

    def _set_square_and_pos(self):
        """
        Determines and sets the target square and, if applicable, the piece's
        file.

        This method processes the move notation to extract the target square
        of the move. It also sets the piece's file for moves where such
        information is implied, particularly for pawn moves.

        Note:
            For castling moves, it calls `get_castling_square` to get the
            target square.
        """

        if self._abr_move == 'O-O' or self._abr_move == 'O-O-O':
            self.square = self._abr_move
            self.square_pos = convert_from_algebraic_notation(
                self._get_castleling_square()
            )
            return

        # See if the position of the piece is given as int

        if (
            self._abr_move[1] in '12345678'
            and self.piece_name != PieceName.PAWN
        ):
            self.row = int(self._abr_move[1]) - 1

        # take the last two characters of the move, this should be the square
        # the piece wants to move to

        self.square = self._abr_move[-2:]
        if len(self._abr_move) == 4:
            if self._abr_move[1] in 'abcdefgh':
                self.piece_file = self._abr_move[1]

        if self.piece_name == PieceName.PAWN:
            # TODO: Check this, it may be wrong
            # We cannot put the file here because this can be an
            # en passant move, so the file should be put later

            if '=' in self.move:
                self.piece_file = self._abr_move[0]
                if 'x' in self.move:
                    self.square = self._abr_move[1:3]
                else:
                    self.square = self._abr_move[:2]
            else:
                self.piece_file = self._abr_move[0]

        self.square_pos = convert_from_algebraic_notation(self.square)

    def _set_coronation(self):
        """
        Determines if the move involves a pawn coronation and sets the
        corresponding piece.
        """
        if self.piece_name == PieceName.PAWN:
            if self.square[1] == '8' or self.square[1] == '1':
                piece_to = self._abr_move[-1]
                for piece_name in PieceName:
                    if piece_name.value[1] == piece_to:
                        self.coronation_into = piece_name
                        return

    def _set_is_capture(self):
        """
        Determines if the move involves a capture
        """

        piece = self.board.get_square_or_piece(
            row=self.square_pos[0],
            column=self.square_pos[1],
        )

        if isinstance(piece, Piece):
            if piece.color.value != self.player_turn.value:
                self.is_capture = True
            return

    def _set_abreviate_move(self):
        """
        Cleans the move string to remove special characters.

        This method removes special characters from the move string, such as
        'x' for captures and '+' for check. The cleaned string is stored in
        the `_abr_move` attribute.

        Returns:
            str: The cleaned move string.
        """

        move = self.move.replace('x', '').replace('+', '').replace('#', '').replace('=', '')
        if move[0] == 'P':  # pawn move
            move = move[1:]

        self._abr_move = move

    def _get_castleling_square(self) -> str:
        """
        Calculates and returns the target square for a castling move.

        This method is called when the move is identified as a castling move
        ('O-O' or 'O-O-O'). It determines the target square based on the
        player's color and the side of the castling.

        Returns:
            str: The algebraic notation of the target square for the castling
            move.
        """

        if self.move == 'O-O':
            self.castleling_side = RookSide.KING
            return 'g1' if self.player_turn == PieceColor.WHITE else 'g8'

        if self.move == 'O-O-O':
            self.castleling_side = RookSide.QUEEN
            return 'c1' if self.player_turn == PieceColor.WHITE else 'c8'

    def __str__(self):
        print('-' * 50)
        print(f'Piece: {self.piece_name}')
        print(f'Piece abbreviation: {self.piece_abbreviation}')
        print(f'Piece file: {self.piece_file}')
        print(f'Square: {self.square}')
        print('-' * 5)
        print(f'Move: {self.move}')
        print(f'Move to compare: {self.move_to_compare}')
        print(f'abr move: {self._abr_move}')
        if self.piece_name == PieceName.PAWN:
            print(f'Coronation into: {self.coronation_into}')
        return '-' * 50
