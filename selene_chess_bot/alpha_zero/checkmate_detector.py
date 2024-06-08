from game import Game


class CheckmateDetector:

    def __init__(
        self,
        fen: str,
    ):
        self.fen = fen
        self.game: Game = Game.parse_fen(fen)

