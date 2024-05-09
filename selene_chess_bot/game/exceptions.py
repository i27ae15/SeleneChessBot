class InvalidMoveError(Exception):

    """
    Exception raised when an invalid move is made.
    """

    def __init__(self, message: str = 'Invalid move'):
        self.message = message
        super().__init__(self.message)
