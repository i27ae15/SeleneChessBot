class BoardAlreadyInitializedError(Exception):

    message = 'Board is already initialized.'

    def __init__(self):
        super().__init__(self.message)


class KingAlreadyOnBoardError(Exception):

    message = '{king_color} King is already on the board.'

    def __init__(self, king_color: str):
        self.message = self.message.replace('{king_color}', king_color)
        super().__init__(self.message)


class SpaceAlreadyOccupiedError(Exception):

    message = 'Space is already occupied.'

    def __init__(self):
        super().__init__(self.message)
