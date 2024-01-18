from pieces.utilites import PieceColor, PieceName, RookSide


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

    def __init__(self, move: str, player_turn: PieceColor) -> None:
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
        """

        self.move = move
        self.player_turn = player_turn
        self.is_castleling: bool = False
        self.castleling_side: RookSide | None = None

        self.piece_abbreviation: str | None = None
        self.piece: PieceName | None = None
        self.piece_file: str | None = None
        self.square: str | None = None

        self._abr_move: str = move.replace('x', '').replace('+', '')
        self.set_move_information()

    def set_piece(self, look_for_pawn: bool = True) -> PieceName:
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

        found = False

        if look_for_pawn:
            if len(self._abr_move) == 2:
                # this will mean that the piece is a pawn so add the P
                self.piece_abbreviation = 'P'
                self.piece = PieceName.PAWN
                found = True

        if self._abr_move == 'O-O' or self._abr_move == 'O-O-O':
            # the piece we want to move is the king
            self.is_castleling = True
            self.piece_abbreviation = 'K'
            self.piece = PieceName.KING
            found = True

        abr = self._abr_move[0]

        for piece in PieceName:
            if piece.value[1] == abr:
                self.piece_abbreviation = piece.value[1]
                self.piece = piece
                found = True
                break

        if not found:
            raise ValueError('Invalid move')

        return self.piece

    def get_castleling_square(self) -> str:
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

    def set_square_and_pos(self):
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
            self.square = self.get_castleling_square()

        # take the last two characters of the move, this should be the square
        # the piece wants to move to

        self.square = self._abr_move[-2:]
        if len(self._abr_move) == 4:
            if self._abr_move[1] in 'abcdefgh':
                self.piece_file = self._abr_move[1]

    def set_move_information(self):
        """
        Parses the move string to extract and set detailed move information.

        This method is a comprehensive handler that sets the piece type, the
        target square, and other move-specific details. It is responsible for
        ensuring that all relevant attributes of the move are accurately
        determined and set.

        Raises:
            ValueError: If the move notation is invalid or cannot be parsed.
        """
        if len(self._abr_move) == 2:
            # we know that this is a pawn
            # set the piece
            # check that the first letter is within the range of a-h
            if self._abr_move[0] not in 'abcdefgh':
                raise ValueError('Invalid move')
            self.piece = PieceName.PAWN
            self.piece_file = self._abr_move[0]
            self.piece_abbreviation = PieceName.PAWN.value[1]
            self.square = self._abr_move
            return

        # if we haven't get the piece yet, let's get it here
        self.set_piece()

        # we now have to get the square where the piece is being move to
        # and the pos of the piece if given
        self.set_square_and_pos()

    def __str__(self):
        print('-' * 50)
        print(f'Piece: {self.piece}')
        print(f'Piece abbreviation: {self.piece_abbreviation}')
        print(f'Piece file: {self.piece_file}')
        print(f'Square: {self.square}')
        print(f'Move: {self.move}')
        return '-' * 50
