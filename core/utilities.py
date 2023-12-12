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


def convert_to_algebraic_notation(row: int, column: int) -> str:
    """
        Converts a position in the form of integers to a string in
        algebraic notation.
    """

    row = ALGEBRAIC_NOTATION['row'][row]
    column = ALGEBRAIC_NOTATION['column'][column]

    return column + row
