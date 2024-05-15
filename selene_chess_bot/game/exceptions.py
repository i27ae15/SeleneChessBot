class InvalidMoveError(Exception):

    """
    Exception raised when an invalid move is made.
    """

    message: str = 'Invalid move'

    def __init__(self, where: str):
        self.message += f' at {where}'
        super().__init__(self.message)
