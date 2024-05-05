ALGEBRAIC_NOTATION = {
    'row': {
        0: '1',
        1: '2',
        2: '3',
        3: '4',
        4: '5',
        5: '6',
        6: '7',
        7: '8'
    },
    'column': {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: 'h'
    }
}

INITIAL_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
INITIAL_BOARD_HASH = 1317592813748421116


def convert_to_algebraic_notation(row: int, column: int) -> str:
    """
        Converts a position in the form of integers to a string in
        algebraic notation.
    """

    row = ALGEBRAIC_NOTATION['row'][row]
    column = ALGEBRAIC_NOTATION['column'][column]

    return column + row


def convert_from_algebraic_notation(position: str) -> tuple:
    """
        Converts a position in algebraic notation to a tuple of integers.

        TODO: Implement the color of the piece when the king if being castled
    """

    row = int(position[1]) - 1
    column = ord(position[0]) - 97

    return (row, column)
