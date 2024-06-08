from game import Game

from pieces.utilites import PieceName, PieceColor
from pieces import King


class CheckDetector:

    def __init__(
        self,
        fen: str,
        get_checks_on_position: bool = True,
    ):
        self.initial_fen = fen

        # Private attributes
        self.__checks_initialized: bool = False
        self.__checks_on_position: list[str] = None
        self.__initial_game: Game = Game.parse_fen(fen)

        # initializers
        self.__checks_on_position_initializer(get_checks_on_position)

    @property
    def checks_on_position(self) -> list[str]:
        if self.__checks_on_position is None:
            print("Checks not initialized. \
                  Call get_checks_on_position_initializer() first.")

        return self.__checks_on_position

    def __checks_on_position_initializer(
        self,
        get_checks_on_position: bool,
    ) -> None:
        if self.__checks_initialized or not get_checks_on_position:
            return

        self.set_checks_on_position()
        self.__checks_initialized = True

    def set_checks_on_position(self) -> list[str]:
        """
        Get the list of checks on the current position.

        Returns:
        --------
        List[str]
            The list of checks on the current position.
        """

        if self.__checks_on_position is not None:
            return self.__checks_on_position

        legal_moves = self.__initial_game.get_legal_moves(
            show_as_list=True,
            show_in_algebraic=True,
        )
        initial_color: PieceColor = self.__initial_game.player_turn

        possible_checks: list[str] = []

        print("Checking for checks on the position...")
        print("Legal moves:", legal_moves)

        for move in legal_moves:

            game = Game.parse_fen(self.initial_fen)
            game.move_piece(move)

            # check for checks on the position after the move
            king: King = game.board.get_piece(
                color=initial_color.opposite(),
                piece_name=PieceName.KING,
            )[0]

            if king.is_in_check:
                possible_checks.append(move)

        self.__checks_on_position = possible_checks
        return self.__checks_on_position
